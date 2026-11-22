
def main():
    print("\n========== MINI-COURIER PLANNER ==========")
    print("1. Launch GUI")
    print("2. Launch Terminal Mode")
    print("3. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        import tkinter as tk
        from gui import CourierApp

        root = tk.Tk()
        app = CourierApp(root)
        root.mainloop()

    elif choice == "2":
        from cli import run_terminal
        run_terminal()

    elif choice == "3":
        print("Exiting Mini-Courier Planner.")

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
