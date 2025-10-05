"""
Plugin management system for Ariadne.

This module provides a plugin architecture for extending Ariadne functionality,
with plugin discovery, loading, and lifecycle management.
"""

from __future__ import annotations

import importlib
import inspect
import os
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

try:
    from ariadne.core import get_logger
except ImportError:
    # Fallback for when running as a script
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from ariadne.core import get_logger


class PluginState(Enum):
    """States of a plugin lifecycle."""
    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    DEACTIVATING = "deactivating"
    INACTIVE = "inactive"
    UNLOADING = "unloading"
    ERROR = "error"


class PluginType(Enum):
    """Types of plugins."""
    BACKEND = "backend"
    ROUTER = "router"
    ANALYZER = "analyzer"
    OPTIMIZER = "optimizer"
    VALIDATOR = "validator"
    EXPORTER = "exporter"
    IMPORTER = "importer"
    MIDDLEWARE = "middleware"
    EXTENSION = "extension"


@dataclass
class PluginInfo:
    """Information about a plugin."""
    name: str
    version: str
    description: str
    author: str
    email: Optional[str] = None
    url: Optional[str] = None
    license: Optional[str] = None
    plugin_type: PluginType = PluginType.EXTENSION
    dependencies: List[str] = field(default_factory=list)
    ariadne_version: Optional[str] = None
    python_version: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    entry_point: Optional[str] = None
    config_schema: Optional[Dict[str, Any]] = None


@dataclass
class PluginStatus:
    """Status of a plugin."""
    state: PluginState
    load_time: Optional[float] = None
    init_time: Optional[float] = None
    error_message: Optional[str] = None
    last_error: Optional[Exception] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class PluginError(Exception):
    """Raised when plugin operations fail."""
    pass


class Plugin(ABC):
    """Base class for all plugins."""
    
    def __init__(self):
        """Initialize the plugin."""
        self.logger = get_logger(f"plugin.{self.__class__.__name__}")
        self._info = self.get_info()
        self._status = PluginStatus(state=PluginState.UNLOADED)
        self._config = {}
    
    @abstractmethod
    def get_info(self) -> PluginInfo:
        """Get plugin information."""
        pass
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin with configuration."""
        pass
    
    @abstractmethod
    def activate(self) -> None:
        """Activate the plugin."""
        pass
    
    @abstractmethod
    def deactivate(self) -> None:
        """Deactivate the plugin."""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up plugin resources."""
        pass
    
    @property
    def info(self) -> PluginInfo:
        """Get plugin information."""
        return self._info
    
    @property
    def status(self) -> PluginStatus:
        """Get plugin status."""
        return self._status
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get plugin configuration."""
        return self._config
    
    def _set_state(self, state: PluginState, error_message: Optional[str] = None) -> None:
        """Set plugin state."""
        self._status.state = state
        if error_message:
            self._status.error_message = error_message
        
        self.logger.debug(f"Plugin state changed to {state.value}")
    
    def _set_error(self, error: Exception) -> None:
        """Set plugin error."""
        self._status.state = PluginState.ERROR
        self._status.last_error = error
        self._status.error_message = str(error)
        
        self.logger.error(f"Plugin error: {error}")


class BackendPlugin(Plugin):
    """Base class for backend plugins."""
    
    @abstractmethod
    def get_backend_class(self) -> Type:
        """Get the backend class provided by this plugin."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the backend is available."""
        pass


class RouterPlugin(Plugin):
    """Base class for router plugins."""
    
    @abstractmethod
    def get_router_class(self) -> Type:
        """Get the router class provided by this plugin."""
        pass


class PluginManager:
    """Manager for plugin discovery, loading, and lifecycle."""
    
    def __init__(self, plugin_dirs: Optional[List[str]] = None):
        """
        Initialize the plugin manager.
        
        Args:
            plugin_dirs: Directories to search for plugins
        """
        self.logger = get_logger("plugin_manager")
        
        # Plugin directories
        self.plugin_dirs = plugin_dirs or [
            os.path.join(os.path.dirname(__file__), "builtin"),
            os.path.join(os.path.expanduser("~"), ".ariadne", "plugins"),
            "/usr/local/share/ariadne/plugins",
        ]
        
        # Plugin registry
        self._plugins: Dict[str, Plugin] = {}
        self._plugin_classes: Dict[str, Type[Plugin]] = {}
        
        # Plugin discovery
        self._discovered_plugins: Dict[str, PluginInfo] = {}
        
        # Discover plugins
        self._discover_plugins()
    
    def _discover_plugins(self) -> None:
        """Discover available plugins."""
        self.logger.info("Discovering plugins...")
        
        # Discover built-in plugins
        self._discover_builtin_plugins()
        
        # Discover external plugins
        for plugin_dir in self.plugin_dirs:
            if os.path.exists(plugin_dir):
                self._discover_plugins_in_dir(plugin_dir)
        
        self.logger.info(f"Discovered {len(self._discovered_plugins)} plugins")
    
    def _discover_builtin_plugins(self) -> None:
        """Discover built-in plugins."""
        builtin_dir = os.path.join(os.path.dirname(__file__), "builtin")
        if os.path.exists(builtin_dir):
            self._discover_plugins_in_dir(builtin_dir)
    
    def _discover_plugins_in_dir(self, plugin_dir: str) -> None:
        """Discover plugins in a directory."""
        self.logger.debug(f"Searching for plugins in: {plugin_dir}")
        
        # Add to Python path if not already there
        if plugin_dir not in sys.path:
            sys.path.insert(0, plugin_dir)
        
        # Look for plugin files
        for item in os.listdir(plugin_dir):
            item_path = os.path.join(plugin_dir, item)
            
            if os.path.isfile(item_path) and item.endswith(".py") and not item.startswith("__"):
                # Python file plugin
                module_name = item[:-3]  # Remove .py extension
                self._discover_plugin_module(module_name, plugin_dir)
            elif os.path.isdir(item_path) and not item.startswith("__"):
                # Package plugin
                self._discover_plugin_package(item, plugin_dir)
    
    def _discover_plugin_module(self, module_name: str, plugin_dir: str) -> None:
        """Discover a plugin from a Python module."""
        try:
            # Import module
            module = importlib.import_module(module_name)
            
            # Look for plugin class
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, Plugin) and 
                    obj is not Plugin and 
                    obj.__module__ == module_name):
                    
                    # Get plugin info
                    try:
                        plugin_instance = obj()
                        plugin_info = plugin_instance.get_info()
                        self._discovered_plugins[plugin_info.name] = plugin_info
                        self._plugin_classes[plugin_info.name] = obj
                        
                        self.logger.debug(f"Discovered plugin: {plugin_info.name}")
                    except Exception as e:
                        self.logger.warning(f"Failed to get info for plugin {name}: {e}")
        except Exception as e:
            self.logger.warning(f"Failed to import plugin module {module_name}: {e}")
    
    def _discover_plugin_package(self, package_name: str, plugin_dir: str) -> None:
        """Discover a plugin from a Python package."""
        try:
            # Import package
            module = importlib.import_module(package_name)
            
            # Look for plugin class
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, Plugin) and 
                    obj is not Plugin and 
                    obj.__module__.startswith(package_name)):
                    
                    # Get plugin info
                    try:
                        plugin_instance = obj()
                        plugin_info = plugin_instance.get_info()
                        self._discovered_plugins[plugin_info.name] = plugin_info
                        self._plugin_classes[plugin_info.name] = obj
                        
                        self.logger.debug(f"Discovered plugin: {plugin_info.name}")
                    except Exception as e:
                        self.logger.warning(f"Failed to get info for plugin {name}: {e}")
        except Exception as e:
            self.logger.warning(f"Failed to import plugin package {package_name}: {e}")
    
    def list_discovered_plugins(self) -> List[PluginInfo]:
        """List all discovered plugins."""
        return list(self._discovered_plugins.values())
    
    def list_loaded_plugins(self) -> List[Plugin]:
        """List all loaded plugins."""
        return list(self._plugins.values())
    
    def get_plugin_info(self, name: str) -> Optional[PluginInfo]:
        """Get information about a discovered plugin."""
        return self._discovered_plugins.get(name)
    
    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get a loaded plugin by name."""
        return self._plugins.get(name)
    
    def is_plugin_loaded(self, name: str) -> bool:
        """Check if a plugin is loaded."""
        return name in self._plugins
    
    def is_plugin_available(self, name: str) -> bool:
        """Check if a plugin is available for loading."""
        return name in self._discovered_plugins
    
    def load_plugin(self, name: str, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Load a plugin.
        
        Args:
            name: Plugin name
            config: Plugin configuration
            
        Returns:
            True if plugin was loaded successfully
        """
        if name in self._plugins:
            self.logger.warning(f"Plugin {name} is already loaded")
            return True
        
        if name not in self._discovered_plugins:
            self.logger.error(f"Plugin {name} is not available")
            return False
        
        plugin_info = self._discovered_plugins[name]
        plugin_class = self._plugin_classes[name]
        
        self.logger.info(f"Loading plugin: {name}")
        
        try:
            # Create plugin instance
            plugin = plugin_class()
            plugin._set_state(PluginState.LOADING)
            
            # Record load time
            load_start = time.time()
            
            # Initialize plugin
            plugin._set_state(PluginState.INITIALIZING)
            plugin.initialize(config or {})
            
            # Record init time
            init_start = time.time()
            
            # Activate plugin
            plugin._set_state(PluginState.ACTIVATING)
            plugin.activate()
            
            # Update status
            plugin._status.load_time = load_start
            plugin._status.init_time = init_start
            plugin._set_state(PluginState.ACTIVE)
            
            # Store plugin
            self._plugins[name] = plugin
            
            self.logger.info(f"Plugin {name} loaded successfully")
            return True
            
        except Exception as e:
            plugin._set_error(e)
            self.logger.error(f"Failed to load plugin {name}: {e}")
            return False
    
    def unload_plugin(self, name: str) -> bool:
        """
        Unload a plugin.
        
        Args:
            name: Plugin name
            
        Returns:
            True if plugin was unloaded successfully
        """
        if name not in self._plugins:
            self.logger.warning(f"Plugin {name} is not loaded")
            return True
        
        plugin = self._plugins[name]
        
        self.logger.info(f"Unloading plugin: {name}")
        
        try:
            # Deactivate plugin
            plugin._set_state(PluginState.DEACTIVATING)
            plugin.deactivate()
            
            # Cleanup plugin
            plugin._set_state(PluginState.UNLOADING)
            plugin.cleanup()
            
            # Update status
            plugin._set_state(PluginState.UNLOADED)
            
            # Remove from registry
            del self._plugins[name]
            
            self.logger.info(f"Plugin {name} unloaded successfully")
            return True
            
        except Exception as e:
            plugin._set_error(e)
            self.logger.error(f"Failed to unload plugin {name}: {e}")
            return False
    
    def reload_plugin(self, name: str, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Reload a plugin.
        
        Args:
            name: Plugin name
            config: Plugin configuration
            
        Returns:
            True if plugin was reloaded successfully
        """
        if name in self._plugins:
            if not self.unload_plugin(name):
                return False
        
        return self.load_plugin(name, config)
    
    def load_plugins_by_type(self, plugin_type: PluginType, config: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Load all plugins of a specific type.
        
        Args:
            plugin_type: Type of plugins to load
            config: Plugin configuration
            
        Returns:
            List of loaded plugin names
        """
        loaded_plugins = []
        
        for name, info in self._discovered_plugins.items():
            if info.plugin_type == plugin_type:
                if self.load_plugin(name, config):
                    loaded_plugins.append(name)
        
        return loaded_plugins
    
    def load_all_plugins(self, config: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Load all available plugins.
        
        Args:
            config: Plugin configuration
            
        Returns:
            List of loaded plugin names
        """
        loaded_plugins = []
        
        for name in self._discovered_plugins:
            if self.load_plugin(name, config):
                loaded_plugins.append(name)
        
        return loaded_plugins
    
    def unload_all_plugins(self) -> List[str]:
        """
        Unload all loaded plugins.
        
        Returns:
            List of unloaded plugin names
        """
        unloaded_plugins = []
        
        # Get list of loaded plugins to avoid modifying during iteration
        plugin_names = list(self._plugins.keys())
        
        for name in plugin_names:
            if self.unload_plugin(name):
                unloaded_plugins.append(name)
        
        return unloaded_plugins
    
    def get_plugins_by_type(self, plugin_type: PluginType) -> List[Plugin]:
        """Get all loaded plugins of a specific type."""
        return [
            plugin for plugin in self._plugins.values()
            if plugin.info.plugin_type == plugin_type
        ]
    
    def get_backend_plugins(self) -> List[BackendPlugin]:
        """Get all loaded backend plugins."""
        return self.get_plugins_by_type(PluginType.BACKEND)
    
    def get_router_plugins(self) -> List[RouterPlugin]:
        """Get all loaded router plugins."""
        return self.get_plugins_by_type(PluginType.ROUTER)


# Global plugin manager instance
_global_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """Get the global plugin manager."""
    global _global_plugin_manager
    if _global_plugin_manager is None:
        _global_plugin_manager = PluginManager()
    return _global_plugin_manager


def load_plugin(name: str, config: Optional[Dict[str, Any]] = None) -> bool:
    """
    Load a plugin using the global plugin manager.
    
    Args:
        name: Plugin name
        config: Plugin configuration
        
    Returns:
        True if plugin was loaded successfully
    """
    manager = get_plugin_manager()
    return manager.load_plugin(name, config)


def unload_plugin(name: str) -> bool:
    """
    Unload a plugin using the global plugin manager.
    
    Args:
        name: Plugin name
        
    Returns:
        True if plugin was unloaded successfully
    """
    manager = get_plugin_manager()
    return manager.unload_plugin(name)


def list_plugins() -> List[PluginInfo]:
    """List all discovered plugins using the global plugin manager."""
    manager = get_plugin_manager()
    return manager.list_discovered_plugins()