import os
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox
from threading import Thread


def install_pyinstaller():
    try:
        subprocess.run(["pip", "install", "pyinstaller"], check=True)
        messagebox.showinfo("Success", "PyInstaller installed successfully.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to install PyInstaller.")


def check_pyinstaller():
    try:
        subprocess.run(["pyinstaller", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except FileNotFoundError:
        return False


def package_script(script_path, additional_file, output_dir, console_mode, icon_path, progress_label):
    if not script_path:
        messagebox.showwarning("No File Selected", "Please select a Python script.")
        return

    cmd = ["pyinstaller", "--onefile"]
    if not console_mode:
        cmd.append("--noconsole")
    if additional_file:
        cmd.extend(["--add-data", f"{additional_file};."])
    if icon_path:
        cmd.extend(["--icon", icon_path])
    cmd.extend(["--distpath", output_dir, script_path])

    def run_packaging():
        try:
            progress_label.set("Packaging... Please wait.")
            subprocess.run(cmd, check=True)
            progress_label.set("Packaging complete!")
            messagebox.showinfo("Success", f"Executable created in {output_dir}")
        except subprocess.CalledProcessError:
            progress_label.set("Error during packaging.")
            messagebox.showerror("Error", "Failed to package the executable.")

    Thread(target=run_packaging).start()


def select_file(label, variable):
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        variable.set(file_path)
        label.configure(text=f"Selected: {os.path.basename(file_path)}")


def select_additional_file(label, variable):
    file_path = filedialog.askopenfilename()
    if file_path:
        variable.set(file_path)
        label.configure(text=f"Selected: {os.path.basename(file_path)}")


def select_icon_file(label, variable):
    file_path = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
    if file_path:
        variable.set(file_path)
        label.configure(text=f"Selected: {os.path.basename(file_path)}")


def main():
    if not check_pyinstaller():
        install_pyinstaller()
        return

    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue") 

    app = ctk.CTk()
    app.title("Py to Exe - V2")
    app.geometry("500x550")

    script_path = ctk.StringVar(value="")
    additional_file = ctk.StringVar(value="")
    icon_path = ctk.StringVar(value="")
    progress_label = ctk.StringVar(value="Ready to package.")

    ctk.CTkLabel(app, text="Py to Exe V2", font=("Arial", 20)).pack(pady=10)

    script_label = ctk.CTkLabel(app, text="No file selected", font=("Arial", 12), text_color="gray")
    script_label.pack(pady=5)
    ctk.CTkButton(app, text="Select Python Script", command=lambda: select_file(script_label, script_path)).pack(pady=5)

    additional_label = ctk.CTkLabel(app, text="No additional file selected", font=("Arial", 12), text_color="gray")
    additional_label.pack(pady=5)
    ctk.CTkButton(app, text="Select Additional File (Optional)", command=lambda: select_additional_file(additional_label, additional_file)).pack(pady=5)

    icon_label = ctk.CTkLabel(app, text="No icon file selected", font=("Arial", 12), text_color="gray")
    icon_label.pack(pady=5)
    ctk.CTkButton(app, text="Select Icon File (Optional, beta)", command=lambda: select_icon_file(icon_label, icon_path)).pack(pady=5)

    ctk.CTkLabel(app, textvariable=progress_label, font=("Arial", 12), text_color="green").pack(pady=10)

    def confirm_and_package(console_mode):
        if not script_path.get():
            messagebox.showwarning("No File Selected", "Please select a Python script.")
            return

        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return

        confirmation = messagebox.askyesno(
            "Confirm Packaging",
            f"Are you sure you want to package?\n\n"
            f"Script: {script_path.get()}\n"
            f"Additional File: {additional_file.get() if additional_file.get() else 'None'}\n"
            f"Icon File: {icon_path.get() if icon_path.get() else 'None'}\n"
            f"Output Directory: {output_dir}\n"
            f"Mode: {'With Console' if console_mode else 'No Console'}"
        )
        if confirmation:
            package_script(script_path.get(), additional_file.get(), output_dir, console_mode, icon_path.get(), progress_label)

    ctk.CTkButton(app, text="Package with Console", command=lambda: confirm_and_package(console_mode=True)).pack(pady=10)
    ctk.CTkButton(app, text="Package without Console", command=lambda: confirm_and_package(console_mode=False)).pack(pady=10)

    ctk.CTkButton(app, text="Exit", command=app.quit).pack(pady=10)

    app.mainloop()


if __name__ == "__main__":
    main()