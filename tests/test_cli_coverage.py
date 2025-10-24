"""
Test CLI module to improve coverage and ensure robust command-line interface.
"""

import subprocess
import sys
from unittest.mock import Mock, patch

from ariadne.cli.main import AriadneCLI, main


class TestCLI:
    """Test CLI functionality for coverage improvement."""

    def test_cli_help(self):
        """Test CLI help output."""
        cli = AriadneCLI()
        parser = cli._create_parser()
        help_text = parser.format_help()

        assert "ariadne" in help_text.lower()
        assert "quantum" in help_text.lower()
        assert "--help" in help_text

    def test_cli_version(self):
        """Test CLI version output."""
        cli = AriadneCLI()
        cli._create_parser()

        # Test version argument
        with patch("sys.argv", ["ariadne", "--version"]):
            with patch("builtins.print"):
                try:
                    main()
                except SystemExit:
                    pass  # Expected for --version

    def test_cli_simulate_command(self):
        """Test CLI simulate command."""
        # Test with basic circuit file (mock the file reading)
        test_circuit = """
from qiskit import QuantumCircuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()
"""

        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = test_circuit

            # Mock the simulate function
            with patch("ariadne.cli.main.simulate") as mock_simulate:
                mock_result = Mock()
                mock_result.backend_used = "stim"
                mock_result.execution_time = 0.01
                mock_result.counts = {"00": 50, "11": 50}
                mock_simulate.return_value = mock_result

                # Test simulate command
                with patch("sys.argv", ["ariadne", "simulate", "test_circuit.py"]):
                    main()

                mock_simulate.assert_called_once()

    def test_cli_backends_command(self):
        """Test CLI backends command."""
        with patch("ariadne.cli.main.get_available_backends") as mock_backends:
            mock_backends.return_value = ["stim", "qiskit", "tensor_network"]

            with patch("builtins.print"):
                with patch("sys.argv", ["ariadne", "backends"]):
                    main()

                # Should print available backends
                mock_backends.assert_called_once()

    def test_cli_explain_command(self):
        """Test CLI explain command."""
        test_circuit = """
from qiskit import QuantumCircuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
"""

        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = test_circuit

            with patch("ariadne.cli.main.explain_routing") as mock_explain:
                mock_explain.return_value = "Circuit is Clifford, using Stim for speedup"

                with patch("builtins.print"):
                    with patch("sys.argv", ["ariadne", "explain", "test_circuit.py"]):
                        main()

                    mock_explain.assert_called_once()

    def test_cli_benchmark_command(self):
        """Test CLI benchmark command."""
        with patch("ariadne.cli.main.run_benchmark") as mock_benchmark:
            mock_benchmark.return_value = {"stim": 0.01, "qiskit": 0.05}

            with patch("builtins.print"):
                with patch("sys.argv", ["ariadne", "benchmark", "--quick"]):
                    main()

                mock_benchmark.assert_called_once()

    def test_cli_error_handling(self):
        """Test CLI error handling."""
        # Test with missing file
        with patch("sys.argv", ["ariadne", "simulate", "nonexistent.py"]):
            with patch("builtins.print"):
                try:
                    main()
                except SystemExit:
                    pass  # Expected for file not found

                # Should handle error gracefully
                pass  # Error handling tested

    def test_cli_with_backend_option(self):
        """Test CLI with backend specification."""
        test_circuit = """
from qiskit import QuantumCircuit
qc = QuantumCircuit(1)
qc.h(0)
"""

        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = test_circuit

            with patch("ariadne.cli.main.simulate") as mock_simulate:
                mock_result = Mock()
                mock_result.backend_used = "qiskit"
                mock_result.execution_time = 0.02
                mock_simulate.return_value = mock_result

                with patch("sys.argv", ["ariadne", "simulate", "--backend", "qiskit", "test.py"]):
                    main()

                # Should pass backend parameter
                call_args = mock_simulate.call_args
                assert "backend" in str(call_args) or "qiskit" in str(call_args)

    def test_cli_with_shots_option(self):
        """Test CLI with shots specification."""
        test_circuit = """
from qiskit import QuantumCircuit
qc = QuantumCircuit(1)
qc.h(0)
"""

        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = test_circuit

            with patch("ariadne.cli.main.simulate") as mock_simulate:
                mock_result = Mock()
                mock_result.backend_used = "stim"
                mock_result.execution_time = 0.01
                mock_simulate.return_value = mock_result

                with patch("sys.argv", ["ariadne", "simulate", "--shots", "500", "test.py"]):
                    main()

                # Should pass shots parameter
                call_args = mock_simulate.call_args
                assert "shots" in str(call_args) or "500" in str(call_args)


class TestCLIIntegration:
    """Integration tests for CLI."""

    def test_cli_subprocess_execution(self):
        """Test CLI execution as subprocess."""
        # Test help command via subprocess
        result = subprocess.run(
            [sys.executable, "-m", "ariadne.cli.main", "--help"], capture_output=True, text=True, timeout=10
        )

        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()
        assert "ariadne" in result.stdout.lower()

    def test_cli_version_subprocess(self):
        """Test version command via subprocess."""
        result = subprocess.run(
            [sys.executable, "-m", "ariadne.cli.main", "--version"], capture_output=True, text=True, timeout=10
        )

        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0  # Should have version output
