from datetime import date
import flet as ft

class Pantry(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.new_item = ft.TextField(hint_text="What's in the pantry?", expand=True)
        self.items = ft.Column()
        self.filter = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Pantry"
                ),
                ft.Tab(
                    text="Fridge"
                ),
                ft.Tab(
                    text="Freezer"    
                ),
            ],
            expand=1
        )
        
        self.items_left = ft.Text("0 items left")
        self.date_picker = DatePickerManager(self.page)
        self.quatity_selector=QuantityButtons(self.page)
        
        self.controls = [
            ft.Column(
              controls=
              [
                ft.Row(
                    controls=[
                        self.new_item,
                        ft.FloatingActionButton(
                            icon=ft.Icons.ADD, on_click=self.add_clicked
                        ),
                    ],
                ),
                ft.Row(
                    controls=
                    [
                        ft.RadioGroup(
                            content=ft.Row(
                                [
                                    ft.Radio(value="pantry", label="Pantry"),
                                    ft.Radio(value="fridge", label="Fridge"),
                                    ft.Radio(value="freezer",label="Freezer")
                                ]
                            )
                       ),
                        
                        self.date_picker.get_ui(),
                        self.quatity_selector.display_ui(),
                    ],
                ),
              ],  
            ),
            ft.Column(
                spacing=24,
                controls=[
                    self.filter,
                    self.items,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.items_left,
                            ft.OutlinedButton(
                                text="Empty", on_click=self.clear_clicked
                            ),
                        ],
                    ),
                ],
            ),
        ]
        
    def add_clicked(self,e):
        if self.new_item.value:
            item = FoodItem(self.new_item.value, self.quatity_selector.get_quantity, self.item_status_change, self.item_delete)
            self.items.controls.append(item)
            self.new_item.value = ""
            self.new_item.focus()
            self.update()
    
    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for item in self.items.controls:
            item.visible = (
                status == "Pantry"
                or (status == "Freezer")
                or (status == "Fridge")
            )
            if not item.in_stock:
                count += 1
        self.items_left.value = f"{count} active item(s) left"
    
    def clear_clicked(self, e):
        for item in self.items.controls[:]:
            if item.in_stock:
                self.item_delete(item)
    
    def tabs_changed(self,e):
        self.update()
        
    def item_status_change(self,e):
        self.update()
        
    def item_delete(self, item):
        self.items.controls.remove(item)
        self.update()
        
        
class FoodItem(ft.Column):
    def __init__(self, item_name, quantity, item_category, item_delete):
        super().__init__()
        self.in_stock = False
        self.item_name = item_name
        self.item_quantity = quantity
        self.item_category = item_category
        self.item_delete = item_delete
        self.display_item = ft.Checkbox(
            value=False, label=self.item_name, on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=1)
        
        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_item,
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
                self.edit_name,
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Update Item",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_item, self.edit_view] 
        
    def status_changed(self,e):
        self.in_stock = self.display_item.value
        self.item_status_change()
     
    def edit_clicked(self, e):
        self.edit_name.value = self.display_item.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_item.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        self.item_delete(self)   

class DatePickerManager:
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
    page.adaptive = True
    page.add(ft.Text(value="Welcome to your kitchen"))
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.window.prevent_close = True
    
    def on_window_event(e: ft.ControlEvent):
        if e.data == "close":
            page.window.prevent_close = False
            page.window.destroy()
            
    page.window.on_event = on_window_event
    pantry = Pantry(page)
    page.add(pantry)
    page.update()
    
ft.app(main)