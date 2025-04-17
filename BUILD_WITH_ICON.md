# Building 2048 Game with Custom Icon

This document explains how to build the 2048 game application with a custom icon that will appear in the Windows taskbar, window titlebar, and as the application icon when built with Nuitka in onefile mode.

## Prerequisites

Ensure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

This will install Flask, Nuitka, and other dependencies needed for the build process.

## Icon Files

The application uses a custom icon located in the `assets` directory:
- `assets/2048_icon.ico` - Icon file used for the application

## Building with Nuitka

You can build the application using the provided build script:

```bash
python nuitka_build.py
```

This will create a standalone executable in the `dist` directory with the following features:
- Custom application icon
- Single executable file (onefile mode)
- No console window
- All assets included

### Manual Nuitka Build

If you prefer to run the Nuitka build command directly, you can use:

```bash
python -m nuitka --standalone --onefile --windows-icon-from-ico=assets/2048_icon.ico --enable-plugin=tk-inter --include-data-dir=assets=assets --windows-disable-console --output-dir=dist main.py
```

## Icon Integration

The icon is integrated in two ways:
1. At runtime, the application loads the icon file to display in the window titlebar
2. During the Nuitka build process, the icon is embedded into the executable file using the `--windows-icon-from-ico` parameter

## Troubleshooting

If you encounter issues with the icon:

1. Ensure the icon file exists in the correct location
2. Check that the icon file is a valid .ico file
3. For runtime issues, check for error messages in the console output
4. For build issues, try running the build with verbose output using `--verbose`

## Notes for Developers

If you wish to modify the icon:
1. Replace the file at `assets/2048_icon.ico` with your custom icon
2. The icon should be in .ico format with multiple sizes (16x16, 32x32, 48x48, 64x64, etc.)
3. Rebuild the application using the build script 