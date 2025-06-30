import pytest


@pytest.fixture
def complex_spec_tree(tmp_path):
    """Create a complex SpecTree structure for testing."""
    # Create directory structure
    (tmp_path / "components").mkdir()
    (tmp_path / "styles").mkdir()
    (tmp_path / "docs").mkdir()
    
    # Create component files
    header = tmp_path / "components" / "header.md"
    header.write_text("## Header Component\nThis is the header.")
    
    footer = tmp_path / "components" / "footer.md"
    footer.write_text("## Footer Component\nThis is the footer.")
    
    # Create style files
    colors = tmp_path / "styles" / "colors.md"
    colors.write_text("### Colors\n- Primary: #007acc\n- Secondary: #6c757d")
    
    typography = tmp_path / "styles" / "typography.md"
    typography.write_text("### Typography\n- Font: Inter\n- Size: 16px")
    
    # Create design system file that references styles
    design_system = tmp_path / "design-system.md"
    design_system.write_text("# Design System\n\n@styles/colors.md\n\n@styles/typography.md")
    
    # Create documentation
    api_docs = tmp_path / "docs" / "api.md"
    api_docs.write_text("# API Documentation\nEndpoints and usage.")
    
    # Create main app specification
    app_spec = tmp_path / "app.md"
    app_spec.write_text("""# Application Specification

@components/header.md

@design-system.md

## Main Content
This is the main application content.

@components/footer.md

## Documentation
@docs/api.md
""")
    
    return {
        'app_spec': app_spec,
        'design_system': design_system,
        'components': {
            'header': header,
            'footer': footer,
        },
        'styles': {
            'colors': colors,
            'typography': typography,
        },
        'docs': {
            'api': api_docs,
        }
    }


@pytest.fixture
def circular_reference_files(tmp_path):
    """Create files with circular references for testing."""
    file_a = tmp_path / "a.md"
    file_b = tmp_path / "b.md"
    file_c = tmp_path / "c.md"
    
    # Create circular chain: a -> b -> c -> a
    file_a.write_text("File A content\n@b.md")
    file_b.write_text("File B content\n@c.md")
    file_c.write_text("File C content\n@a.md")
    
    return {'a': file_a, 'b': file_b, 'c': file_c}


@pytest.fixture
def mixed_valid_invalid_refs(tmp_path):
    """Create file with mix of valid and invalid @ references."""
    valid_ref = tmp_path / "valid.md"
    valid_ref.write_text("This is valid content.")
    
    main_file = tmp_path / "mixed.md"
    main_file.write_text("""# Mixed References Test

@valid.md

This is some text @invalid_inline.md that should not be processed.

  @invalid_indent.md

@@invalid_double.md

@

@invalid_extension.txt

The end.
""")
    
    return {'main': main_file, 'valid': valid_ref}