import pytest
from spectree.core import render, CircularReferenceError


class TestBasicRendering:
    """Test basic SpecTree rendering functionality."""
    
    def test_render_file_without_references(self, tmp_path):
        """Test rendering a simple markdown file with no @ references."""
        content = "# Hello World\n\nThis is a simple markdown file."
        file_path = tmp_path / "simple.md"
        file_path.write_text(content)
        
        result = render(file_path)
        assert result == content
    
    def test_render_file_with_single_reference(self, tmp_path):
        """Test rendering a file with one @ reference."""
        # Create referenced file
        referenced_content = "This is referenced content."
        referenced_file = tmp_path / "referenced.md"
        referenced_file.write_text(referenced_content)
        
        # Create main file
        main_content = "# Main File\n\n@referenced.md\n\nEnd of main."
        main_file = tmp_path / "main.md"
        main_file.write_text(main_content)
        
        result = render(main_file)
        expected = "# Main File\n\nThis is referenced content.\n\nEnd of main."
        assert result == expected
    
    def test_render_file_with_multiple_references(self, tmp_path):
        """Test rendering a file with multiple @ references."""
        # Create referenced files
        ref1 = tmp_path / "ref1.md"
        ref1.write_text("Content 1")
        
        ref2 = tmp_path / "ref2.md"
        ref2.write_text("Content 2")
        
        # Create main file
        main_content = "# Main\n\n@ref1.md\n\nMiddle text\n\n@ref2.md\n\nEnd"
        main_file = tmp_path / "main.md"
        main_file.write_text(main_content)
        
        result = render(main_file)
        expected = "# Main\n\nContent 1\n\nMiddle text\n\nContent 2\n\nEnd"
        assert result == expected


class TestNestedReferences:
    """Test nested @ references (references within referenced files)."""
    
    def test_nested_references(self, tmp_path):
        """Test that references within referenced files are resolved."""
        # Create deepest file
        deep_file = tmp_path / "deep.md"
        deep_file.write_text("Deep content")
        
        # Create middle file that references deep file
        middle_file = tmp_path / "middle.md"
        middle_file.write_text("Middle start\n@deep.md\nMiddle end")
        
        # Create main file that references middle file
        main_file = tmp_path / "main.md"
        main_file.write_text("Main start\n@middle.md\nMain end")
        
        result = render(main_file)
        expected = "Main start\nMiddle start\nDeep content\nMiddle end\nMain end"
        assert result == expected
    
    def test_multiple_nested_references(self, tmp_path):
        """Test complex nested reference patterns."""
        # Create leaf files
        leaf1 = tmp_path / "leaf1.md"
        leaf1.write_text("Leaf 1")
        
        leaf2 = tmp_path / "leaf2.md"
        leaf2.write_text("Leaf 2")
        
        # Create branch files (@ must be at start of line per spec)
        branch1 = tmp_path / "branch1.md"
        branch1.write_text("Branch 1:\n@leaf1.md")
        
        branch2 = tmp_path / "branch2.md"
        branch2.write_text("Branch 2:\n@leaf2.md")
        
        # Create root file
        root = tmp_path / "root.md"
        root.write_text("Root\n@branch1.md\n@branch2.md\nEnd")
        
        result = render(root)
        expected = "Root\nBranch 1:\nLeaf 1\nBranch 2:\nLeaf 2\nEnd"
        assert result == expected


class TestPathResolution:
    """Test path resolution behavior."""
    
    def test_relative_path_resolution(self, tmp_path):
        """Test that paths are resolved relative to the referencing file."""
        # Create subdirectory
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        
        # Create file in subdirectory
        sub_file = subdir / "sub.md"
        sub_file.write_text("Sub content")
        
        # Create main file that references subdirectory file
        main_file = tmp_path / "main.md"
        main_file.write_text("Main\n@subdir/sub.md\nEnd")
        
        result = render(main_file)
        expected = "Main\nSub content\nEnd"
        assert result == expected
    
    def test_parent_directory_references(self, tmp_path):
        """Test references to parent directories using ../."""
        # Create parent file
        parent_file = tmp_path / "parent.md"
        parent_file.write_text("Parent content")
        
        # Create subdirectory
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        
        # Create file in subdirectory that references parent
        sub_file = subdir / "sub.md"
        sub_file.write_text("Sub start\n@../parent.md\nSub end")
        
        result = render(sub_file)
        expected = "Sub start\nParent content\nSub end"
        assert result == expected
    
    def test_nested_directory_structure(self, tmp_path):
        """Test complex directory structures with multiple levels."""
        # Create nested directory structure
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        
        shared_dir = tmp_path / "shared"
        shared_dir.mkdir()
        
        # Create shared file
        header_file = shared_dir / "header.md"
        header_file.write_text("Shared header")
        
        # Create docs file that references shared
        overview_file = docs_dir / "overview.md"
        overview_file.write_text("Overview\n@../shared/header.md\nContent")
        
        # Create main file that references docs
        main_file = tmp_path / "main.md"
        main_file.write_text("Main\n@docs/overview.md\nEnd")
        
        result = render(main_file)
        expected = "Main\nOverview\nShared header\nContent\nEnd"
        assert result == expected


class TestSyntaxValidation:
    """Test @ operator syntax validation."""
    
    def test_valid_reference_syntax(self, tmp_path):
        """Test that valid @ syntax is recognized."""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text("Referenced")
        
        main_file = tmp_path / "main.md"
        main_file.write_text("@ref.md")
        
        result = render(main_file)
        assert result == "Referenced"
    
    def test_invalid_reference_with_leading_whitespace(self, tmp_path):
        """Test that @ with leading whitespace is not treated as reference."""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text("Referenced")
        
        main_file = tmp_path / "main.md"
        main_file.write_text("  @ref.md")
        
        result = render(main_file)
        assert result == "  @ref.md"  # Should be left unchanged
    
    def test_invalid_reference_not_at_line_start(self, tmp_path):
        """Test that @ not at line start is not treated as reference."""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text("Referenced")
        
        main_file = tmp_path / "main.md"
        main_file.write_text("text @ref.md")
        
        result = render(main_file)
        assert result == "text @ref.md"  # Should be left unchanged
    
    def test_invalid_double_at_symbol(self, tmp_path):
        """Test that @@ is not treated as reference."""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text("Referenced")
        
        main_file = tmp_path / "main.md"
        main_file.write_text("@@ref.md")
        
        result = render(main_file)
        assert result == "@@ref.md"  # Should be left unchanged
    
    def test_invalid_empty_reference(self, tmp_path):
        """Test that @ alone is not treated as reference."""
        main_file = tmp_path / "main.md"
        main_file.write_text("@")
        
        result = render(main_file)
        assert result == "@"  # Should be left unchanged
    
    def test_invalid_non_markdown_extension(self, tmp_path):
        """Test that non-.md files are not treated as references."""
        ref_file = tmp_path / "ref.txt"
        ref_file.write_text("Text content")
        
        main_file = tmp_path / "main.md"
        main_file.write_text("@ref.txt")
        
        result = render(main_file)
        assert result == "@ref.txt"  # Should be left unchanged


class TestErrorHandling:
    """Test error handling for various failure scenarios."""
    
    def test_file_not_found_error(self, tmp_path):
        """Test that missing files raise FileNotFoundError."""
        main_file = tmp_path / "main.md"
        main_file.write_text("@nonexistent.md")
        
        with pytest.raises(FileNotFoundError):
            render(main_file)
    
    def test_circular_reference_error_direct(self, tmp_path):
        """Test detection of direct circular references."""
        # Create files that reference each other
        file_a = tmp_path / "a.md"
        file_b = tmp_path / "b.md"
        
        file_a.write_text("@b.md")
        file_b.write_text("@a.md")
        
        with pytest.raises(CircularReferenceError):
            render(file_a)
    
    def test_circular_reference_error_indirect(self, tmp_path):
        """Test detection of indirect circular references."""
        # Create files: a -> b -> c -> a
        file_a = tmp_path / "a.md"
        file_b = tmp_path / "b.md"
        file_c = tmp_path / "c.md"
        
        file_a.write_text("@b.md")
        file_b.write_text("@c.md")
        file_c.write_text("@a.md")
        
        with pytest.raises(CircularReferenceError):
            render(file_a)
    
    def test_self_reference_error(self, tmp_path):
        """Test that self-references are detected as circular."""
        file_a = tmp_path / "a.md"
        file_a.write_text("@a.md")
        
        with pytest.raises(CircularReferenceError):
            render(file_a)


class TestWhitespacePreservation:
    """Test whitespace and formatting preservation."""
    
    def test_preserve_empty_lines(self, tmp_path):
        """Test that empty lines are preserved."""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text("Line 1\n\nLine 3")
        
        main_file = tmp_path / "main.md"
        main_file.write_text("Start\n\n@ref.md\n\nEnd")
        
        result = render(main_file)
        expected = "Start\n\nLine 1\n\nLine 3\n\nEnd"
        assert result == expected
    
    def test_preserve_leading_trailing_whitespace(self, tmp_path):
        """Test that leading/trailing whitespace in files is preserved."""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text("\nContent\n")
        
        main_file = tmp_path / "main.md"
        main_file.write_text("@ref.md")
        
        result = render(main_file)
        assert result == "\nContent\n"
    
    def test_preserve_indentation(self, tmp_path):
        """Test that indentation is preserved."""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text("    Indented content\n        More indented")
        
        main_file = tmp_path / "main.md"
        main_file.write_text("@ref.md")
        
        result = render(main_file)
        assert result == "    Indented content\n        More indented"


class TestUTF8Encoding:
    """Test UTF-8 encoding handling."""
    
    def test_utf8_content(self, tmp_path):
        """Test that UTF-8 content is handled correctly."""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text("Hello 世界 🌍", encoding='utf-8')
        
        main_file = tmp_path / "main.md"
        main_file.write_text("@ref.md", encoding='utf-8')
        
        result = render(main_file)
        assert result == "Hello 世界 🌍"


class TestEdgeCases:
    """Test various edge cases and boundary conditions."""
    
    def test_empty_file(self, tmp_path):
        """Test rendering empty files."""
        empty_file = tmp_path / "empty.md"
        empty_file.write_text("")
        
        result = render(empty_file)
        assert result == ""
    
    def test_reference_to_empty_file(self, tmp_path):
        """Test referencing an empty file."""
        empty_file = tmp_path / "empty.md"
        empty_file.write_text("")
        
        main_file = tmp_path / "main.md"
        main_file.write_text("Before\n@empty.md\nAfter")
        
        result = render(main_file)
        assert result == "Before\n\nAfter"
    
    def test_file_with_only_references(self, tmp_path):
        """Test file containing only @ references."""
        ref1 = tmp_path / "ref1.md"
        ref1.write_text("Content 1")
        
        ref2 = tmp_path / "ref2.md"
        ref2.write_text("Content 2")
        
        main_file = tmp_path / "main.md"
        main_file.write_text("@ref1.md\n@ref2.md")
        
        result = render(main_file)
        assert result == "Content 1\nContent 2"
    
    def test_reference_on_last_line_without_newline(self, tmp_path):
        """Test reference on last line without trailing newline."""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text("Referenced content")
        
        main_file = tmp_path / "main.md"
        main_file.write_text("@ref.md", newline='')  # No trailing newline
        
        result = render(main_file)
        assert result == "Referenced content"