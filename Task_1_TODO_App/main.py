import flet as fl

class Task(fl.UserControl):
    def __init__(self, task_name, task_delete, task_status_change):
            super().__init__()
            self.completed = False
            self.task_name = task_name
            self.task_delete = task_delete
            self.task_status_change = task_status_change

    def build(self):
        self.display_task = fl.Checkbox(
            value=False, label=self.task_name, on_change=self.state_change
        )

        self.edit_name = fl.TextField(expand=1)

        self.display = fl.Row(
            alignment=fl.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=fl.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                fl.Row(
                    spacing=0,
                    controls=[
                        fl.IconButton(
                            icon=fl.icons.CREATE_OUTLINED,
                            tooltip="Edit Task",
                            on_click=self.edit_click,
                        ),
                        fl.IconButton(
                            icon=fl.icons.DELETE_OUTLINED,
                            tooltip="Delete Task",
                            on_click=self.delete_click,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = fl.Row(
            visible=False,
            alignment=fl.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=fl.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                fl.IconButton(
                    icon=fl.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=fl.colors.GREEN,
                    tooltip="Update Task",
                    on_click=self.save_click,
                ),
            ],
        )

        return fl.Column(controls=[self.display, self.edit_view])
    
    def edit_click(self, e):
        self.edit_name.value = self.display_task.label
        self.display.visible = False
        self.edit_view.visible = True
        self.update()

    def save_click(self, e):
        self.display_task.label = self.edit_name.value
        self.display.visible = True
        self.edit_view.visible = False
        self.update()

    def state_change(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)

    def delete_click(self, e):
        self.task_delete(self)
        
    

class ToDoApp(fl.UserControl):
    def build(self):
            self.heading = fl.Text("Welcome to TODO Application", text_align=fl.alignment.center)
            self.new_item = fl.TextField(hint_text="Add a new Task", width=300, expand=True)
            self.tasks = fl.Column()

            self.filter = fl.Tabs(
                selected_index=0,
                on_change=self.tabs_change,
                tabs=[
                    fl.Tab(text="all"),
                    fl.Tab(text="active"),
                    fl.Tab(text="completed"),
                ],
            )
                
            return fl.Column(
                        width=600,
                        controls=[
                            self.heading,
                            fl.Row(
                                controls=[
                                    self.new_item,
                                    fl.FloatingActionButton(icon=fl.icons.ADD, on_click=self.add_click),
                                ],
                            ), 
                            fl.Column(
                                spacing=25,
                                controls=[
                                    self.filter,
                                    self.tasks,
                                ],
                            ),
                        ],
                    )
    
    def add_click(self, e):
        task = Task(self.new_item.value, self.task_delete, self.task_status_change)
        self.tasks.controls.append(task)
        self.new_item.value = ""
        self.update()

    def task_status_change(self, e):
        self.update()

    def task_delete(self, task):
        if task in self.tasks.controls:
            self.tasks.controls.remove(task)
        self.update()

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and task.completed == False)
                or (status == "completed" and task.completed)
            )

            super().update()

    def tabs_change(self, e):
        self.update()
            

def main(page: fl.Page):

    page.title = "TODO List By Tushin Kulshreshtha"
    page.horizontal_alignment = fl.CrossAxisAlignment.CENTER
    page.theme_mode = fl.ThemeMode.DARK

    todo = ToDoApp()

    page.add(todo)


fl.app(target=main)