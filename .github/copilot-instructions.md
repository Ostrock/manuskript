## Summary

Manuskript is an open-source novel writing application built with Python 3.8+ and PyQt5. It helps fiction authors plan, organize, and write their manuscripts using features like outlining (Snowflake method, Three-Act structure), character management, world-building, plot tracking, and distraction-free writing modes. Projects are saved as folder structures (Git-friendly) or single .msk ZIP files.

## Purpose of This Document
You are a senior software engineer brought in to help onboard new contributors to the Manuskript codebase. This document serves as a comprehensive guide to understanding the architecture, coding conventions, and key components of the project.
When contributing, please refer to this document to familiarize yourself with the code structure and best practices.
When planning you should always aim for design pattern adoption and clean code principles.
After the implementation you have to update this document to reflect the changes made and any new patterns introduced.
You should also lint the code using ruff and fix any inconsistencies with the coding guidelines outlined below especially aiming to adhere to all styling PEP8 conventions and others.
To get the most recent and relevant information about the language program, frameworks and libraries used in this project you should always use context7 to query for the latest documentation and best practices.

## Terminology

- **Outline Item** - A scene, chapter, or folder in the manuscript hierarchy. Stored in `outline/` as Markdown files with MMD metadata headers.
- **POV** - Point of View character for a scene. Stored as character ID reference (e.g., `POV: 3`).
- **Cork Board** - Visual view showing scenes as index cards that can be rearranged.
- **Snowflake Method** - Writing methodology: start with one-sentence summary, expand iteratively.
- **MMD** - MultiMarkdown format used for metadata headers in outline files (`Title:`, `POV:`, `Status:`).
- **Label/Status** - User-defined tags for organizing scenes (e.g., "First Draft", "Needs Review").
- **Flat Data Model** - `mdlFlatData` stores project-wide metadata (title, author, summary).
- **Goal** - Word count target for scenes, chapters, or entire project.

## Architecture

Manuskript follows Qt's Model-View pattern with four separate domain models:

- `mdlOutline` (outlineModel) - Tree of scenes/chapters with Markdown content
- `mdlCharacter` (characterModel) - List of characters with attributes
- `mdlPlots` (plotModel) - Plot structures with steps/resolutions
- `mdlWorld` (worldModel) - World-building tree (OPML format)

**Key architectural files:**
- [mainWindow.py](manuskript/mainWindow.py) - Central coordinator (~2300 lines), orchestrates all views and models
- [models/outlineItem.py](manuskript/models/outlineItem.py) - Core data structure for manuscript items
- [load_save/version_1.py](manuskript/load_save/version_1.py) - Project serialization with file-level caching
- [functions/__init__.py](manuskript/functions/__init__.py) - Utility functions including `safeTranslate()`, `wordCount()`
- [enums.py](manuskript/enums.py) - Column enums for all models (Outline, Character, Plot, World)

**Cross-model references use string IDs:**
```python
# Scene references character by ID
pov_id = item.data(Outline.POV)  # Returns "3"
character = mdlCharacter.getCharacterByID(pov_id)
```

**Save format:** Folder structure with `MANUSKRIPT` version marker, `infos.txt` metadata, `outline/` folder with numbered `.md` files, `characters/` with `ID-name.txt` files.

## Task Planning and Problem-Solving

- Before implementing a feature, identify which model(s) are affected and trace the data flow from UI → model → persistence.
- Check for existing similar implementations before adding new code. Search in `manuskript/ui/` for UI patterns and `manuskript/models/` for model patterns.
- When modifying save/load, always ensure backward compatibility. New fields must have defaults for older projects.
- For UI changes, consider both folder and ZIP save formats behave identically.
- When adding search support to a new model, follow the mixin pattern in `searchableModel.py`.

## Coding Guidelines

### Naming Conventions (Legacy)
The codebase uses camelCase for classes and functions (non-PEP8 legacy).
Adopt the scout rule from clean code by robert c. martin adn changing the names adopt the PEP8 style assuring then it is consistent across the codebase and fixing the calls to it in other files as well.
All new code should follow PEP8 naming conventions (snake_case for functions/variables, PascalCase for classes).
```python
# Existing pattern - follow it
class outlineItem:      # camelCase class (legacy)
    def wordCount(self):  # camelCase method
```

### Qt Patterns
- Use `beginResetModel()`/`endResetModel()` for bulk model changes, `dataChanged.emit()` for single items.
- Store `QPersistentModelIndex` instead of `QModelIndex` when keeping references across operations.
- Never access Qt widgets from non-UI threads. Use signals to communicate results back to the main thread.
- Connect signals after widget initialization, not before, to avoid missed emissions.

### Translation
- Use `safeTranslate(qApp, "Context", "String")` for dynamic strings outside QObject classes.
- Use `self.tr("String")` inside QObject subclasses.
- Translation context should match the class name where the string appears.

### Error Handling
- Catch specific exceptions, not bare `except:`. Log errors with the `LOGGER` from `manuskript.logging`.
- For file operations, handle `FileNotFoundError`, `PermissionError`, `OSError` explicitly.

### Model References
- Cross-model references store IDs as strings, not object references.
- Always validate that referenced IDs exist when loading (graceful degradation for deleted items).

## Common Gotchas

- **QModelIndex invalidation**: Indices become invalid after model changes. Use `QPersistentModelIndex` for storage.
- **Signal-slot timing**: Ensure signals are connected before any code that might emit them.
- **Cache in version_1.py**: The global `cache` dict prevents redundant writes. Clear it with `clearSaveCache()` when switching projects.
- **Status/Label values**: These are stored as indices (integers), not display strings. Use `settings.py` lists to map.
- **Text format**: Outline item text may contain Markdown or HTML depending on editor mode. Use `HTML2PlainText()` for plain text.

## Verification Commands

After making changes, verify with:
1. `python -m pytest manuskript/tests/ -v` - Run unit tests
2. `python bin/manuskript` - Launch application to test manually
3. Open sample project in `sample-projects/` to verify load/save works

## File Organization

```
manuskript/
├── models/           # Qt models (outlineModel, characterModel, etc.)
├── ui/               # UI widgets and views
│   ├── editors/      # Text editors (MDEditView, textEditView)
│   ├── views/        # Specialized views (corkView, outlineView)
│   └── highlighters/ # Syntax highlighters
├── exporter/         # Export plugins (Pandoc-based)
├── importer/         # Import plugins (OPML, Markdown, etc.)
├── load_save/        # Project serialization
├── functions/        # Utility functions
└── tests/            # pytest tests with fixtures
```
