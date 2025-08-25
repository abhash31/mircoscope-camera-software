def menu_bar(self):
    menu_bar = self.menuBar()

    # File Menu
    file_menu = menu_bar.addMenu("File")
    open_menu_item = file_menu.addMenu("Open")

    open_image_action = open_menu_item.addAction("Open Image")
    open_image_action.triggered.connect(self.open_image)
    open_image_action.setShortcut("Ctrl+I")

    open_camera_action = open_menu_item.addAction("Open Camera")
    open_camera_action.triggered.connect(self.start_stop_camera_feed)
    open_camera_action.setShortcut("Ctrl+C")

    file_menu.addSeparator()

    save_action = file_menu.addAction("Save Current Frame")
    save_action.triggered.connect(self.save_current_frame)
    save_action.setShortcut("Ctrl+S")

    # Tools Menu
    tools_menu = menu_bar.addMenu("Tools")

    self.ruler_action = tools_menu.addAction("Enable Measurement Tool")
    self.ruler_action.setCheckable(True)
    self.ruler_action.triggered.connect(self.toggle_ruler_from_menu)
    self.ruler_action.triggered.connect(self.toggle_top_toolbox)
    self.ruler_action.setShortcut("Ctrl+M")

    clear_rulers_action = tools_menu.addAction("Clear All Measurements")
    clear_rulers_action.triggered.connect(self.clear_all_rulers)