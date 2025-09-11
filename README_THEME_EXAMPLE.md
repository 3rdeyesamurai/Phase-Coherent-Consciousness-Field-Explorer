# ttkthemes Dark Theme Example

This repository demonstrates how to use the `ttkthemes` package to apply beautiful dark themes to tkinter/ttk applications.

## 🎯 What This Example Shows

### ✅ Completed Tasks:
- [x] **Install ttkthemes package** - Successfully installed via pip
- [x] **Create simple example script** - `theme_example.py` with comprehensive demo
- [x] **Show how to change to dark theme** - Dynamic theme switching with dropdown
- [x] **Test the example** - Verified working with multiple dark themes

### 🎨 Features Demonstrated:
- **Easy Theme Installation**: `pip install ttkthemes`
- **Simple Theme Application**: One-line theme switching
- **Dynamic Theme Switching**: Change themes at runtime
- **Professional Dark Themes**: Multiple beautiful dark theme options
- **Widget Consistency**: All tkinter/ttk widgets styled uniformly

## 🚀 Quick Start

### 1. Install ttkthemes
```bash
pip install ttkthemes
```

### 2. Basic Usage
```python
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

# Create root window
root = tk.Tk()

# Initialize ttkthemes style
style = ThemedStyle(root)

# Apply dark theme
style.set_theme("equilux")  # Dark theme with blue accents

# Create your widgets normally
button = ttk.Button(root, text="Click me!")
button.pack()

root.mainloop()
```

### 3. Run the Example
```bash
python theme_example.py
```

## 🎨 Available Dark Themes

The example demonstrates these beautiful dark themes:

- **equilux**: Dark theme with blue accents (recommended)
- **black**: Pure black background
- **darkly**: Green-accented dark theme
- **solar**: Orange-accented dark theme
- **cyborg**: Cyberpunk-inspired theme
- **slate**: Dark slate theme
- **superhero**: Blue-grey accents
- **cosmo**: Modern dark theme
- **flatly**: Flat dark theme
- **journal**: Minimal dark theme

## 📋 Example Features

The `theme_example.py` script includes:

- **Theme Selector**: Dropdown to switch between themes
- **Demo Widgets**: Buttons, progress bars, entry fields, checkboxes, radio buttons
- **Real-time Updates**: Instant theme switching
- **Theme Descriptions**: Information about each theme
- **Error Handling**: Graceful handling of theme application errors

## 🔧 Integration with Existing Code

To add dark themes to your existing tkinter application:

1. **Install ttkthemes**:
   ```bash
   pip install ttkthemes
   ```

2. **Modify your code**:
   ```python
   # Add these imports
   from ttkthemes import ThemedStyle

   # Replace your style initialization
   # OLD: style = ttk.Style()
   # NEW:
   style = ThemedStyle(root)
   style.set_theme("equilux")  # Choose your preferred dark theme
   ```

3. **That's it!** All your existing ttk widgets will automatically use the dark theme.

## 🎯 Advanced Usage

### Custom Theme Configuration
```python
# Configure specific widget styles
style.configure('TButton', font=('Arial', 10, 'bold'))
style.configure('TLabel', foreground='#ffffff')

# Apply to specific widgets
button = ttk.Button(root, text="Styled Button", style='TButton')
```

### Theme Information
```python
# Get available themes
available_themes = style.themes
print("Available themes:", available_themes)

# Get current theme
current_theme = style.theme_use()
print("Current theme:", current_theme)
```

## 🐛 Troubleshooting

### Common Issues:
1. **Import Error**: Make sure ttkthemes is installed (`pip install ttkthemes`)
2. **Theme Not Found**: Check theme name spelling against `style.themes`
3. **Widget Not Styled**: Ensure you're using ttk widgets, not tk widgets

### Theme Compatibility:
- All themes work on Windows, macOS, and Linux
- Some themes may render slightly differently on different platforms
- The `equilux` theme is recommended as the most consistent dark theme

## 📚 Resources

- **ttkthemes Documentation**: https://ttkthemes.readthedocs.io/
- **tkinter Documentation**: https://docs.python.org/3/library/tkinter.html
- **Theme Gallery**: Run `theme_example.py` to see all themes in action

## 🎉 Success!

The ttkthemes package has been successfully installed and demonstrated. You now have a working example of how to apply beautiful dark themes to your tkinter applications with minimal code changes!

**Key Takeaway**: Adding dark themes to tkinter apps is now as simple as:
1. `pip install ttkthemes`
2. `from ttkthemes import ThemedStyle`
3. `style = ThemedStyle(root)`
4. `style.set_theme("equilux")`
