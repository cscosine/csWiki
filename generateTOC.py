#!/usr/bin/env python3

import sys
import re
from pathlib import Path

from dataclasses import dataclass, field
from typing import List, Tuple


# --------------------------------------------------
# Utilities
# --------------------------------------------------
@dataclass
class Report:
    errors : List[str] = field(default_factory=list) 
    warnings : List[str] = field(default_factory=list) 
    infos : List[str] = field(default_factory=list) 
    
    def append(self, other: "Report") -> None:
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.infos.extend(other.infos)

    # --- ANSI colors (private inside class) ---
    _RED = "\033[31m"
    _YELLOW = "\033[33m"
    _BLUE = "\033[34m"
    _RESET = "\033[0m"
    _BOLD = "\033[1m"

    def print(self) -> None:
        if(len(self.errors) + len(self.warnings) + len(self.infos)) > 0:
            print(f"{self._YELLOW}{self._BOLD}---------- REPORT ----------{self._RESET}")
            self._print_block("ERROR", self.errors, self._RED, bold=True)
            self._print_block("WARNING", self.warnings, self._YELLOW, bold=True)
            self._print_block("INFO", self.infos, self._BLUE)
            print(f"{self._YELLOW}{self._BOLD}----------------------------{self._RESET}")

    def _print_block(self, label: str, messages: List[str], color: str, bold: bool = False):
        if not messages:
            return

        style = self._BOLD if bold else ""
        for msg in messages:
            print(f"{color}{style}[{label}]{self._RESET} {msg}")

## Replace TOC block with new content
def replace_toc(content, toc) -> Tuple[str, bool]:

    report = Report()
    TOC_BEGIN = "<!-- TOC BEGIN -->"
    TOC_END = "<!-- TOC END -->"

    has_toc = TOC_BEGIN in content and TOC_END in content
    if not has_toc:
        return content, False
    
    pattern = re.compile(
        rf"{re.escape(TOC_BEGIN)}.*?{re.escape(TOC_END)}",
        re.DOTALL,
    )
    return re.sub(pattern, f"{TOC_BEGIN}\n{toc}\n{TOC_END}", content), True

## Read a file
def read_markdown_file(md_path: Path) -> str | None:
    try:
        return md_path.read_text(encoding="utf-8")
    except OSError as e:
        return None

## Extract all level 1 sections from a markdown file
def extract_level1_sections(content: str) -> List[str]:
    """Return all # Section headings."""
    sections = []
    for line in content.splitlines():
        m = re.match(r"^# (.+)", line.strip())
        if m:
            sections.append(m.group(1))

    return sections

@dataclass
class SectionWithAnchor:
    section: str
    anchor: str

def sectionToSectionWithAnchor(section : str) -> SectionWithAnchor:
    anchor = section.lower().replace(" ", "-")
    return SectionWithAnchor(section=section,anchor=anchor)

def sectionListToSectionWithAnchorList(sections: List[str]) -> List[SectionWithAnchor]:
    sectionAnchorTupleList = []
    for section in sections:
        sectionAnchorTupleList.append(sectionToSectionWithAnchor(section))
    return sectionAnchorTupleList

## Find all markdown files in a folder (excluding a main one)
def find_markdown_files(folder: Path, excludedName : str) -> List[Path]:
    return sorted(
        [f.stem for f in folder.glob("*.md") if f.name != excludedName]
    )

@dataclass
class FindSubFoldersResult:
    paths : List[Path] = field(default_factory=list) 
    report: Report = field(default_factory=Report)

## find subfolders, ignore folders with starting with . and folders that does not contain a file.md with name = parent folder
def find_subfolders(folder: Path) -> FindSubFoldersResult:
    res = FindSubFoldersResult()
    
    for sub in sorted([d for d in folder.iterdir() if d.is_dir()]):
        if sub.name.startswith("."):
            res.report.infos.append(f"Ignoring hidden folder: `{sub.name}`")
            continue

        expected_md = sub / f"{sub.name}.md"
        
        if expected_md.is_file():
            res.paths.append(sub.relative_to(folder))
        else:
            res.report.warnings.append(f"Ignoring folder: `{str(sub)}` because it does not contains `{sub.name}.md` file")

    return res

@dataclass
class FileNode:
    file_name: str
    file_sections: List[SectionWithAnchor] = field(default_factory=list)

@dataclass
class FolderNode:
    folder_name: Path
    main_filename: str
    main_file_sections: List[SectionWithAnchor] = field(default_factory=list)

    subfolders: List["FolderNode"] = field(default_factory=list)
    files: List[FileNode]= field(default_factory=list)

@dataclass
class CreateTreeResult:
    root: FolderNode
    report: Report

def createTree(rootPath : Path, main_filename : str) -> CreateTreeResult:
    report = Report()
    
    root_node = FolderNode(folder_name= Path(""), main_filename = main_filename)

    nodes_to_explore = [(root_node, rootPath)]
    for node, cumulated_path in nodes_to_explore:
        # add sections
        node_main_file_path = cumulated_path / f"{node.main_filename}.md"
        node_content = read_markdown_file(node_main_file_path)
        if(node_content is None):
            report.errors.append(f"Error reading content from {str(node_main_file_path)}")
        else:
            node.main_file_sections = sectionListToSectionWithAnchorList(extract_level1_sections(node_content))

        # files
        files = find_markdown_files(cumulated_path, f"{node.main_filename}.md")
        for fs in files:
            fn = FileNode(file_name = fs)
            fn_file_path = cumulated_path / f"{fn.file_name}.md"
            node_content = read_markdown_file(fn_file_path)
            if(node_content is None):
                report.errors.append(f"Error reading content from {str(fn_file_path)}")
            else:
                fn.file_sections = sectionListToSectionWithAnchorList(extract_level1_sections(node_content))
            node.files.append(fn)

        # subfolders
        subfolders = find_subfolders(cumulated_path)
        report.append(subfolders.report)
        for s in subfolders.paths:
            fn = FolderNode(folder_name= Path(s), main_filename = s)
            node.subfolders.append(fn)
            nodes_to_explore.append((fn, cumulated_path / fn.folder_name))

    return CreateTreeResult(root_node, report)

def printTree(node: FolderNode, indent: str):
    print(f"{indent}- folder: {node.folder_name} main_file: {node.main_filename}")
    for sa in node.main_file_sections:
        print(f"{indent}  * section: {sa.section} anchor: {sa.anchor}")
    for f in node.files:
        print(f"{indent}  - file: {f.file_name}")
        for sa in f.file_sections:
            print(f"{indent}    * section: {sa.section} anchor: {sa.anchor}")
    for s in node.subfolders:
        printTree(s, indent + "  ")

@dataclass
class SectionWithAnchorAndLevel:
    section: str
    anchor: str
    level: int

@dataclass
class TOCFile:
    file_full_path: Path 
    toc_entries: List[SectionWithAnchorAndLevel] = field(default_factory=list)

@dataclass 
class TOCFolder:
    main_file_toc: TOCFile

    files_toc: List[TOCFile] = field(default_factory=list)
    subfolder_toc: List["TOCFolder"] = field(default_factory=list)

def createTOCTreeImpl(rootPath : Path, node: FolderNode) -> TOCFolder:

    nodeTOC = TOCFolder(main_file_toc = TOCFile(file_full_path= rootPath / f"{node.main_filename}.md"))
    # node folder own sections
    #nodeTOC.main_file_toc.toc_entries.append(SectionWithAnchorAndLevel("This File",f"{node.main_filename}.md",0))
    for s in node.main_file_sections:
        nodeTOC.main_file_toc.toc_entries.append(SectionWithAnchorAndLevel(s.section,f"{node.main_filename}.md#{s.anchor}",0))

    # explore subfolders
    subfoldersToc = []
    for s in node.subfolders:
        sTOC = createTOCTreeImpl(rootPath / s.folder_name, s)
        nodeTOC.subfolder_toc.append(sTOC)

        # get its toc from main file
        subfoldersToc.append(SectionWithAnchorAndLevel(f"Subfolder {s.folder_name}", str(s.folder_name / f"{s.main_filename}.md"),0))
        for te in sTOC.main_file_toc.toc_entries:
            subfoldersToc.append(SectionWithAnchorAndLevel(te.section, str(s.folder_name / te.anchor), te.level + 1))


    # explore sibling files
    for nf in node.files:
        sTOC = TOCFile(file_full_path= rootPath / f"{nf.file_name}.md")
        nodeTOC.main_file_toc.toc_entries.append(SectionWithAnchorAndLevel(f"File {nf.file_name}",f"{nf.file_name}.md",0))
        for s in nf.file_sections:
            # add to file toc
            sTOC.toc_entries.append(SectionWithAnchorAndLevel(s.section,f"#{s.anchor}",0))
            # add to folder toc
            nodeTOC.main_file_toc.toc_entries.append(
                SectionWithAnchorAndLevel(s.section, f"{nf.file_name}.md" + f"#{s.anchor}",1)
            )
        nodeTOC.files_toc.append(sTOC)

    # last, add the prepared subfoldersToc
    for st in subfoldersToc:
        nodeTOC.main_file_toc.toc_entries.append(st)

    return nodeTOC

def finalizeTOCTree(node: TOCFolder, parent: TOCFolder):
    if parent is not None:
        parentEntry = SectionWithAnchorAndLevel(f"../{parent.main_file_toc.file_full_path.stem}", f"../{parent.main_file_toc.file_full_path.name}", 0)
        node.main_file_toc.toc_entries = [parentEntry] + node.main_file_toc.toc_entries

    parentEntry = SectionWithAnchorAndLevel(f"../{node.main_file_toc.file_full_path.stem}", f"{node.main_file_toc.file_full_path.name}", 0)
    for f in node.files_toc:
        f.toc_entries = [parentEntry] + f.toc_entries

    for f in node.subfolder_toc:
        finalizeTOCTree(f, node)

def createTOCTree(rootPath : Path, node: FolderNode) -> TOCFolder:
    root = createTOCTreeImpl(rootPath, node)
    finalizeTOCTree(root, None)
    return root


def printTOCFile(node: TOCFile):
    print(f"{node.file_full_path}")
    for s in node.toc_entries:
        print(f"{"  "*s.level}- section: {s.section} anchor: {s.anchor}")
    print()

def printTOCTree(node: TOCFolder):
    printTOCFile(node.main_file_toc)
    for f in node.files_toc:
        printTOCFile(f)
    for f in node.subfolder_toc:
        printTOCTree(f)

def write_toc_file(node: TOCFile) -> Report:
    report = Report()
    # Build TOC string
    lines = []
    lines.append("**Table Of Contents**")
    for s in node.toc_entries:
        indent = "  " * s.level
        lines.append(f"{indent}- [{s.section}]({s.anchor})")
    toc_string = "\n".join(lines)

    # Read existing content (if file exists)
    existing_content = read_markdown_file(node.file_full_path)
    if existing_content is None:
        report.errors.append(f"Error reading {str(node.file_full_path)}")
    else:
        # Let your custom logic modify content
        (updated_content, result) = replace_toc(existing_content, toc_string)
        if result == False:
            report.warnings.append(f"No TOC section found in {str(node.file_full_path)}")

        # Write back to file
        try:
            node.file_full_path.write_text(updated_content, encoding="utf-8")
        except OSError:
            report.errors.append(f"Error writing to {str(node.file_full_path)}")
    
    return report

def write_toc_on_files(node: TOCFolder) -> Report:
    # Update main file
    report = write_toc_file(node.main_file_toc)

    # Update other files in this folder
    for f in node.files_toc:
        report.append(write_toc_file(f))

    # Recurse into subfolders
    for subfolder in node.subfolder_toc:
        report.append(write_toc_on_files(subfolder))

    return report


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("🚀 Generating full recursive TOCs...\n")

    root = Path("./docs")

    treeRoot = createTree(rootPath=root, main_filename= "index")
    printTree(treeRoot.root, "")
    ## check report
    if len(treeRoot.report.errors) > 0:
        treeRoot.report.print()
        print("\033[31m❌ Errors during tree generation, please fix.\033[0m")
        sys.exit(-1)

    report = treeRoot.report

    tocNodeRoot = createTOCTree(rootPath=root, node= treeRoot.root)
    printTOCTree(tocNodeRoot)
    
    write_report = Report()
    write_report = write_toc_on_files(tocNodeRoot)
    report.append(write_report)
    report.print()
    if len(report.errors) > 0:
        print("\033[31m❌ Errors during TOC write to files, please fix.\033[0m")
        sys.exit(-1)


    print("\033[32m✅ Execution completed successfully.\033[0m")
    sys.exit(0)