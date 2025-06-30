import subprocess
import sys


class TestCLIFileInput:
    """Test CLI with file path argument."""
    
    def test_cli_with_file_argument(self, tmp_path):
        """Test CLI accepts file path and prints rendered output to stdout."""
        # Create a simple SpecTree file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Document\n\nThis is a test.")
        
        # Run CLI with file argument
        result = subprocess.run(
            [sys.executable, "-m", "spectree.cli", str(test_file)],
            capture_output=True,
            text=True,
            cwd=tmp_path
        )
        
        assert result.returncode == 0
        assert result.stdout == "# Test Document\n\nThis is a test."
        assert result.stderr == ""
    
    def test_cli_with_file_containing_references(self, tmp_path):
        """Test CLI processes @ references correctly."""
        # Create referenced file
        ref_file = tmp_path / "intro.md"
        ref_file.write_text("## Introduction\n\nWelcome!")
        
        # Create main file with reference
        main_file = tmp_path / "main.md"
        main_file.write_text("# Main Document\n\n@intro.md\n\nEnd.")
        
        # Run CLI
        result = subprocess.run(
            [sys.executable, "-m", "spectree.cli", str(main_file)],
            capture_output=True,
            text=True,
            cwd=tmp_path
        )
        
        assert result.returncode == 0
        expected = "# Main Document\n\n## Introduction\n\nWelcome!\n\nEnd."
        assert result.stdout == expected
        assert result.stderr == ""


class TestCLIStdinInput:
    """Test CLI with stdin input."""
    
    def test_cli_with_stdin_no_references(self, tmp_path):
        """Test CLI accepts input from stdin when no file argument provided."""
        input_content = "# Stdin Test\n\nContent from stdin."
        
        # Run CLI with stdin input
        result = subprocess.run(
            [sys.executable, "-m", "spectree.cli"],
            input=input_content,
            capture_output=True,
            text=True,
            cwd=tmp_path
        )
        
        assert result.returncode == 0
        assert result.stdout == input_content
        assert result.stderr == ""
    
    def test_cli_with_stdin_containing_references(self, tmp_path):
        """Test CLI processes references from stdin relative to current directory."""
        # Create referenced file in current directory
        ref_file = tmp_path / "header.md"
        ref_file.write_text("# Header from File")
        
        # Input with reference
        input_content = "@header.md\n\nContent from stdin."
        
        # Run CLI with stdin input
        result = subprocess.run(
            [sys.executable, "-m", "spectree.cli"],
            input=input_content,
            capture_output=True,
            text=True,
            cwd=tmp_path
        )
        
        assert result.returncode == 0
        expected = "# Header from File\n\nContent from stdin."
        assert result.stdout == expected
        assert result.stderr == ""


class TestCLIErrorHandling:
    """Test CLI error handling and exit codes."""
    
    def test_cli_file_not_found_error(self, tmp_path):
        """Test CLI exits with code 1 and error to stderr for missing file."""
        nonexistent_file = tmp_path / "nonexistent.md"
        
        result = subprocess.run(
            [sys.executable, "-m", "spectree.cli", str(nonexistent_file)],
            capture_output=True,
            text=True,
            cwd=tmp_path
        )
        
        assert result.returncode == 1
        assert result.stdout == ""
        assert "not found" in result.stderr.lower() or "no such file" in result.stderr.lower()
    
    def test_cli_file_with_missing_reference_error(self, tmp_path):
        """Test CLI exits with code 1 for file containing missing reference."""
        # Create main file with missing reference
        main_file = tmp_path / "main.md"
        main_file.write_text("# Main\n\n@missing.md\n\nEnd.")
        
        result = subprocess.run(
            [sys.executable, "-m", "spectree.cli", str(main_file)],
            capture_output=True,
            text=True,
            cwd=tmp_path
        )
        
        assert result.returncode == 1
        assert result.stdout == ""
        assert "not found" in result.stderr.lower()
    
    def test_cli_circular_reference_error(self, tmp_path):
        """Test CLI exits with code 1 for circular references."""
        # Create circular reference files
        file_a = tmp_path / "a.md"
        file_b = tmp_path / "b.md"
        
        file_a.write_text("File A\n@b.md")
        file_b.write_text("File B\n@a.md")
        
        result = subprocess.run(
            [sys.executable, "-m", "spectree.cli", str(file_a)],
            capture_output=True,
            text=True,
            cwd=tmp_path
        )
        
        assert result.returncode == 1
        assert result.stdout == ""
        assert "circular" in result.stderr.lower() or "cycle" in result.stderr.lower()
    
    def test_cli_stdin_with_missing_reference_error(self, tmp_path):
        """Test CLI exits with code 1 for stdin input with missing reference."""
        input_content = "# Test\n\n@nonexistent.md\n\nEnd."
        
        result = subprocess.run(
            [sys.executable, "-m", "spectree.cli"],
            input=input_content,
            capture_output=True,
            text=True,
            cwd=tmp_path
        )
        
        assert result.returncode == 1
        assert result.stdout == ""
        assert "not found" in result.stderr.lower()


class TestCLIHelp:
    """Test CLI help functionality."""
    
    def test_cli_help_flag(self):
        """Test CLI displays help text with --help flag."""
        result = subprocess.run(
            [sys.executable, "-m", "spectree.cli", "--help"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert result.stderr == ""
        
        # Check for key help text elements
        help_text = result.stdout.lower()
        assert "spectree" in help_text
        assert "usage" in help_text or "help" in help_text
        assert "file" in help_text or "path" in help_text
    
    def test_cli_help_short_flag(self):
        """Test CLI shows error for unsupported -h flag (only --help is supported)."""
        result = subprocess.run(
            [sys.executable, "-m", "spectree.cli", "-h"],
            capture_output=True,
            text=True
        )
        
        # Typer doesn't automatically support -h, only --help
        assert result.returncode == 2
        assert "no such option" in result.stderr.lower()
        assert result.stdout == ""


class TestCLIEdgeCases:
    """Test CLI edge cases and boundary conditions."""
    
    def test_cli_empty_file(self, tmp_path):
        """Test CLI handles empty files correctly."""
        empty_file = tmp_path / "empty.md"
        empty_file.write_text("")
        
        result = subprocess.run(
            [sys.executable, "-m", "spectree.cli", str(empty_file)],
            capture_output=True,
            text=True,
            cwd=tmp_path
        )
        
        assert result.returncode == 0
        assert result.stdout == ""
        assert result.stderr == ""
    
    def test_cli_empty_stdin(self, tmp_path):
        """Test CLI handles empty stdin correctly."""
        result = subprocess.run(
            [sys.executable, "-m", "spectree.cli"],
            input="",
            capture_output=True,
            text=True,
            cwd=tmp_path
        )
        
        assert result.returncode == 0
        assert result.stdout == ""
        assert result.stderr == ""
    
    def test_cli_file_with_utf8_content(self, tmp_path):
        """Test CLI handles UTF-8 content correctly."""
        utf8_file = tmp_path / "utf8.md"
        utf8_content = "# UTF-8 Test 🌍\n\nHello 世界!"
        utf8_file.write_text(utf8_content, encoding='utf-8')
        
        result = subprocess.run(
            [sys.executable, "-m", "spectree.cli", str(utf8_file)],
            capture_output=True,
            text=True,
            cwd=tmp_path
        )
        
        assert result.returncode == 0
        assert result.stdout == utf8_content
        assert result.stderr == ""