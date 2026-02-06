"""Mobile Kitchen - main UI module

Lightweight Flet UI demonstrating a pantry list with expiration
date picking and a simple quantity selector.

Run:
    pip install flet
    python src/main.py

This file contains the following high-level components:
- Pantry: the main composite view
- FoodItem: a single item control
- DatePickerManager: helper to manage a DatePicker overlay
- QuantityButtons: plus/minus quantity selector
"""

from datetime import date
import flet as ft

class Pantry(ft.Column):
    """Pantry view composite.

    Contains UI for adding pantry items, filtering by storage type,
    selecting expiration dates, and choosing quantities.
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.new_item = ft.TextField(hint_text="What's in the pantry?", expand=True)
        self.items = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            
        )
        self.filter = ft.Tabs(
            tab_alignment=ft.TabAlignment.CENTER,
            selected_index=0,
            animation_duration=300,
            on_change=self.tabs_changed,
            tabs=[
                ft.Tab(
                    text="Pantry",
                    
                ),
                ft.Tab(
                    text="Fridge",
                    
                ),
                ft.Tab(
                    text="Freezer",
                    
                ),
            ],
            expand_loose=1
        )
        
        
        
        self.items_left = ft.Text("0 items")
        self.date_picker = DatePickerManager(self.page)
        self.quatity_selector=QuantityButtons(self.page)
        self.item_category = ""
        
        self.add_item = ft.AlertDialog(
            title=ft.Text("Add Item"),
            content=ft.Column(
                controls=[
                    self.new_item,
                    ft.RadioGroup(
                            content=ft.Row(
                                [
                                    ft.Radio(value="pantry", label="Pantry"),
                                    ft.Radio(value="fridge", label="Fridge"),
                                    ft.Radio(value="freezer",label="Freezer")
                                ]
                            ),
                            on_change=self.category_change
                    ),
                    self.date_picker.get_ui(),
                    self.quatity_selector.display_ui(),
                ],
                tight=True,
                scroll=ft.ScrollMode.ADAPTIVE
            ),
            actions=[
                ft.TextButton("Add", on_click=self.add_clicked),
                ft.TextButton("Cancel", on_click=self.close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True,
        )
        
        self.controls = [
            
            ft.Container(
                expand=True,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            value="Welcome to your kitchen",
                            text_align=ft.TextAlign.CENTER,
                            size=20,
                            ),
                        self.filter,
                        ft.Stack(
                            expand=True,
                            controls=[  
                                ft.Container(
                                    content=ft.FloatingActionButton(
                                        icon=ft.Icons.ADD, on_click=self.add_button_clicked
                                    ),
                                    alignment=ft.alignment.bottom_right,
                                    padding=ft.padding.all(16),
                                ),
                                self.items,
                            ]
                        ),
                         
                    ],
                ),
            ),
        ]
        
        
    def close_dialog(self,e):
        self.page.close(self.add_item)
        
    def add_button_clicked(self,e):
        self.page.open(self.add_item)
        
    def add_clicked(self,e):
        if self.new_item.value:
            item = FoodItem(self.new_item.value, self.date_picker.get_date(), self.quatity_selector.get_quantity(), self.item_category, self.item_delete)
            
            self.items.controls.append(item)
            self.new_item.value = ""
            self.new_item.focus()
            self.update()
            self.page.close(self.add_item)
    
    def before_update(self):
        current_tab = self.filter.tabs[self.filter.selected_index].text.lower()
        for item in self.items.controls:
            item.visible = (
                item.item_category == current_tab
            )
            
            
    def clear_clicked(self, e):
        for item in self.items.controls[:]:
            if item.in_stock:
                self.item_delete(item)
    
    def tabs_changed(self,e):
        
        self.update()
        
    def category_change(self,e):
        self.item_category=e.control.value
        self.update()
        return self.item_category
        
    def item_delete(self, item):
        self.items.controls.remove(item)
        self.update()
        
        
class FoodItem(ft.Column):
    """A single food item row with edit/delete and in-stock state.

    Parameters
    - item_name: label shown next to the checkbox
    - quantity: initial quantity for display (not editable here)
    - item_category: category string (pantry/fridge/freezer)
    - item_delete: callback called when the item is deleted
    """
    def __init__(self, item_name, exp_date, quantity, item_category, item_delete):
        super().__init__()
        self.in_stock = False
        self.item_name = item_name
        self.exp_date = exp_date
        self.item_quantity = quantity
        self.item_category = item_category
        self.item_delete = item_delete
        self.display_item = ft.Checkbox(
            value=False, label=self.item_name
        )
        self.edit_item = ft.TextField()
        self.edit_quantity = ft.TextField()
        
        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_item,
                ft.Text(value=self.exp_date),
                self.item_quantity,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CREATE_OUTLINED,
                            tooltip="Edit item",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            tooltip="Delete item",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
                
            ],
        )
        
        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_item,
                ft.Text(value=self.item_category),
                self.edit_quantity,
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Update Item",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view, self.edit_view] 
        
    """def category_changed(self,e):
        self.in_stock = self.display_item.value
        self.category_change()
     """
    def edit_clicked(self, e):
        self.edit_item.value = self.display_item.label
        self.edit_quantity.value = self.item_quantity.value
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_item.label = self.edit_item.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        self.item_delete(self)   

class DatePickerManager:
    """Manage a DatePicker attached to the page overlay.

    The manager creates the DatePicker control, appends it to
    `page.overlay`, and exposes `get_ui()` which returns a small
    control (icon + label) for insertion into other layouts.
    """
    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_date_text = ft.Text("Select Exp. Date")

        # 1. Create the DatePicker control
        self.date_picker = ft.DatePicker(
            on_change=self.handle_date_change,
            on_dismiss=self.handle_dismiss,
            first_date=date(2000, 1, 1),
            last_date=date(2035, 12, 31),
        )

        # 2. Add the DatePicker to the page's overlay
        self.page.overlay.append(self.date_picker)
        self.page.update()

    def handle_date_change(self, e: ft.ControlEvent):
        """Called when the user confirms their date selection."""
        if e.control.value:
            self.selected_date_text.value = f"Exp: {e.control.value.strftime('%Y-%m-%d')}"
            self.page.update()

    def handle_dismiss(self, e: ft.ControlEvent):
        """Called when the date picker is dismissed without selection."""
        print("Date picker dismissed")

    def open_date_picker(self, e):
        """Method to open the date picker dialog."""
        self.page.open(self.date_picker)
    
    def get_date(self):
        return self.selected_date_text.value

    def get_ui(self):
        """Returns the UI components for the class to be added to the page."""
        return ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.CALENDAR_TODAY,
                    on_click=self.open_date_picker,
                ),
                self.selected_date_text,
            ]
        )
        
class QuantityButtons(ft.Row):
    """Simple quantity selector with plus/minus buttons.

    Use `display_ui()` to obtain the Row to insert into layouts. The
    control stores the `ft.Text` instance internally so its value can
    be updated even when called from tests before mounting.
    """
    def __init__(self, page: ft.Page = None, quantity: int = 0):
        super().__init__()
        self.page = page
        self.quantity = quantity
        # Use a direct Text control instead of Ref so tests can call handlers
        # even if the control isn't attached to a page yet.
        self.quantity_text = ft.Text(
            value=str(self.quantity),
            size=20,
            weight=ft.FontWeight.BOLD,
            text_align="center",
            width=50,
        )
    def get_quantity(self):
        return self.quantity_text
    
    def subtract_clicked(self, e):
        if self.quantity > 0:
            self.quantity -= 1
            # Update the displayed text; if the control isn't attached yet,
            # this still updates the Text instance.
            self.quantity_text.value = str(self.quantity)
            # Update UI if attached
            # Try to update the Text control if it's mounted in the UI.
            try:
                self.quantity_text.update()
            except Exception:
                # Fallback: request a full page update if we have a page
                try:
                    if self.page:
                        self.page.update()
                except Exception:
                    pass

    def add_clicked(self, e):
        self.quantity += 1
        self.quantity_text.value = str(self.quantity)
        try:
            self.quantity_text.update()
        except Exception:
            try:
                if self.page:
                    self.page.update()
            except Exception:
                pass

    def display_ui(self):
        return ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="-",
                    on_click=self.subtract_clicked,
                ),
                self.quantity_text,
                ft.ElevatedButton(
                    text="+",
                    on_click=self.add_clicked,
                ),
            ]
        )
        
            
def main(page: ft.Page):
    """Application entrypoint used by ft.app().

    The page object is supplied by Flet. This function builds the
    top-level UI and starts the app.
    """
    page.theme_mode = ft.ThemeMode.DARK
    
    page.adaptive = True
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.window.prevent_close = True
    
    def on_window_event(e: ft.ControlEvent):
        if e.data == "close":
            page.window.prevent_close = False
            page.window.destroy()
    
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            background="#262626",
            primary="#9B8769",
            on_primary="#7F7369"
        ),
        floating_action_button_theme=ft.FloatingActionButtonTheme(
            bgcolor="#7F7369",
            foreground_color="#262626"
        )
    )
    
    page.update()      
    page.window.on_event = on_window_event
    pantry = Pantry(page)
    pantry.expand = True
    page.add(pantry)
    page.update()
    
ft.app(main)