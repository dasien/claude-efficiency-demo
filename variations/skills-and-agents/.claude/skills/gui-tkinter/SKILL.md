---
name: gui-tkinter
description: Python Tkinter GUI development patterns, widget layout, event handling, and MVC architecture for desktop applications.
---

## Tkinter GUI Development

### Application Structure
- Use a class-based approach with a main `App` class inheriting from `tk.Tk`
- Separate GUI layout from business logic using MVC or MVP pattern
- Initialize all widgets in a `_create_widgets()` method
- Bind events in a separate `_bind_events()` method

### Widget Layout
- Use `grid()` for complex layouts, `pack()` for simple vertical/horizontal stacking
- Never mix `grid()` and `pack()` in the same container
- Use `ttk` themed widgets over plain `tk` widgets for modern appearance
- Group related widgets in `LabelFrame` or `Frame` containers

### Layout Best Practices
```python
# Use grid with sticky for responsive layouts
self.entry = ttk.Entry(self.main_frame)
self.entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

# Configure column weights for resizing
self.main_frame.columnconfigure(0, weight=1)
```

### Event Handling
- Use `command=` parameter for button clicks
- Use `bind()` for keyboard events: `widget.bind('<Return>', handler)`
- Use `bind_all()` sparingly — prefer widget-specific bindings
- Event handlers should delegate to controller/business logic, not contain logic themselves
- Use `after()` for delayed or periodic operations, never `time.sleep()` in the main thread

### Common Patterns
```python
class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("300x400")
        self._create_widgets()
        self._bind_events()

    def _create_widgets(self):
        self.display = ttk.Entry(self, font=("Courier", 18))
        self.display.grid(row=0, column=0, columnspan=4, sticky="ew")

    def _bind_events(self):
        self.bind('<Return>', self._on_calculate)
```

### Dialog and Messaging
- Use `messagebox.showerror()` for error dialogs
- Use `messagebox.showinfo()` for informational messages
- Use `simpledialog.askstring()` for simple text input
- For complex dialogs, create custom `Toplevel` windows

### Styling
- Use `ttk.Style()` for consistent theming
- Define styles at application startup, not per-widget
- Use named fonts via `tkFont.Font()` for consistent typography

### Threading
- Never perform long operations on the main thread — use `threading.Thread`
- Update GUI only from the main thread — use `after()` to schedule updates
- Use `queue.Queue` to communicate between worker threads and the main thread

### Testing GUI Code
- Separate all logic from GUI code to enable unit testing without Tkinter
- Test business logic independently
- For integration tests, use `tkinter.Tk()` in test fixtures with `update_idletasks()`
- Consider using `pytest-tk` for automated GUI testing
