import pytest
from spectree.core import render, CircularReferenceError


class TestComplexIntegration:
    """Integration tests using complex fixture scenarios."""
    
    def test_complex_spec_tree_rendering(self, complex_spec_tree):
        """Test rendering a complex multi-level SpecTree."""
        result = render(complex_spec_tree['app_spec'])
        
        # Verify all content is included
        assert "Application Specification" in result
        assert "Header Component" in result
        assert "Footer Component" in result
        assert "Design System" in result
        assert "Primary: #007acc" in result
        assert "Font: Inter" in result
        assert "API Documentation" in result
        assert "main application content" in result
        
        # Verify structure is maintained
        lines = result.split('\n')
        app_spec_idx = next(i for i, line in enumerate(lines) if "Application Specification" in line)
        header_idx = next(i for i, line in enumerate(lines) if "Header Component" in line)
        design_idx = next(i for i, line in enumerate(lines) if "Design System" in line)
        
        # Header should come before design system
        assert header_idx > app_spec_idx
        assert design_idx > header_idx
    
    def test_circular_reference_detection(self, circular_reference_files):
        """Test that circular references are properly detected."""
        with pytest.raises(CircularReferenceError) as exc_info:
            render(circular_reference_files['a'])
        
        # Error message should mention the circular path
        error_msg = str(exc_info.value)
        assert "circular" in error_msg.lower() or "cycle" in error_msg.lower()
    
    def test_mixed_valid_invalid_references(self, mixed_valid_invalid_refs):
        """Test handling of mixed valid/invalid references."""
        result = render(mixed_valid_invalid_refs['main'])
        
        # Valid reference should be resolved
        assert "This is valid content." in result
        
        # Invalid references should be left unchanged
        assert "text @invalid_inline.md that" in result
        assert "  @invalid_indent.md" in result
        assert "@@invalid_double.md" in result
        assert "@invalid_extension.txt" in result
        
        # Standalone @ should remain
        lines = result.split('\n')
        assert any(line.strip() == "@" for line in lines)


class TestRealisticScenarios:
    """Test realistic usage scenarios."""
    
    def test_documentation_system(self, tmp_path):
        """Test a realistic documentation system structure."""
        # Create shared components
        (tmp_path / "shared").mkdir()
        header = tmp_path / "shared" / "header.md"
        header.write_text("# Project Documentation\n\nVersion 1.0")
        
        footer = tmp_path / "shared" / "footer.md"
        footer.write_text("---\n© 2024 Company Name")
        
        # Create section files
        intro = tmp_path / "introduction.md"
        intro.write_text("## Introduction\n\nWelcome to our project.")
        
        guide = tmp_path / "user-guide.md"
        guide.write_text("## User Guide\n\nHow to use the system.")
        
        api = tmp_path / "api-reference.md"
        api.write_text("## API Reference\n\nEndpoint documentation.")
        
        # Create main documentation file
        main_doc = tmp_path / "documentation.md"
        main_doc.write_text("""@shared/header.md

@introduction.md

@user-guide.md

@api-reference.md

@shared/footer.md
""")
        
        result = render(main_doc)
        
        # Verify complete document structure
        assert result.startswith("# Project Documentation")
        assert result.rstrip().endswith("© 2024 Company Name")
        assert "Welcome to our project" in result
        assert "How to use the system" in result
        assert "Endpoint documentation" in result
    
    def test_ai_prompt_system(self, tmp_path):
        """Test an AI prompt composition system."""
        # Create role definitions
        (tmp_path / "roles").mkdir()
        assistant_role = tmp_path / "roles" / "assistant.md"
        assistant_role.write_text("You are a helpful AI assistant.")
        
        expert_role = tmp_path / "roles" / "expert.md"  
        expert_role.write_text("You are an expert in software development.")
        
        # Create instruction modules
        (tmp_path / "instructions").mkdir()
        coding_style = tmp_path / "instructions" / "coding-style.md"
        coding_style.write_text("Follow PEP 8 style guidelines.")
        
        testing = tmp_path / "instructions" / "testing.md"
        testing.write_text("Write comprehensive unit tests.")
        
        # Create specific prompt
        python_prompt = tmp_path / "python-dev-prompt.md"
        python_prompt.write_text("""@roles/expert.md

@instructions/coding-style.md

@instructions/testing.md

## Task
Help the user implement Python features following best practices.
""")
        
        result = render(python_prompt)
        
        assert "expert in software development" in result
        assert "PEP 8 style guidelines" in result
        assert "comprehensive unit tests" in result
        assert "best practices" in result