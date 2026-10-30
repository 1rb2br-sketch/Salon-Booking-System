"""A simple salon booking and discount calculator built with Tkinter."""

import math
import tkinter as tk
from tkinter import messagebox, ttk


DISCOUNT_LIMIT = 150
DISCOUNT_RATE = 0.15


def main():
    """Create and run the salon booking window."""
    root = tk.Tk()
    root.title("Salon Booking System")
    root.geometry("560x680")
    root.minsize(460, 620)
    root.configure(bg="#f7f3ef")

    style = ttk.Style(root)
    style.configure("TLabel", background="#f7f3ef", foreground="#292421")
    style.configure("Title.TLabel", font=("TkDefaultFont", 22, "bold"))
    style.configure("Subtitle.TLabel", font=("TkDefaultFont", 10))
    style.configure("Field.TLabel", font=("TkDefaultFont", 10, "bold"))
    style.configure("TEntry", padding=9)
    style.configure("Primary.TButton", padding=(16, 10), font=("TkDefaultFont", 10, "bold"))
    style.configure("TButton", padding=(12, 9), font=("TkDefaultFont", 10))

    page = ttk.Frame(root, padding=(30, 28))
    page.pack(fill="both", expand=True)
    page.columnconfigure(0, weight=1)

    ttk.Label(page, text="Salon Booking", style="Title.TLabel").grid(
        row=0, column=0, sticky="w"
    )
    ttk.Label(
        page,
        text="Enter the customer and service details to calculate the final price.",
        style="Subtitle.TLabel",
        wraplength=470,
    ).grid(row=1, column=0, sticky="w", pady=(6, 24))

    form = ttk.Frame(page)
    form.grid(row=2, column=0, sticky="ew")
    form.columnconfigure(0, weight=1)

    ttk.Label(form, text="Customer name", style="Field.TLabel").grid(
        row=0, column=0, sticky="w"
    )
    name_entry = ttk.Entry(form)
    name_entry.grid(row=1, column=0, sticky="ew", pady=(7, 18))

    ttk.Label(form, text="Service price (SAR)", style="Field.TLabel").grid(
        row=2, column=0, sticky="w"
    )
    price_entry = ttk.Entry(form)
    price_entry.grid(row=3, column=0, sticky="ew", pady=(7, 18))

    results_frame = tk.Frame(
        page,
        bg="#ffffff",
        highlightbackground="#e8dfd8",
        highlightthickness=1,
        padx=16,
        pady=14,
    )
    results_frame.grid(row=5, column=0, sticky="nsew", pady=(22, 0))
    page.rowconfigure(5, weight=1)
    results_frame.columnconfigure(0, weight=1)

    tk.Label(
        results_frame,
        text="Booking details",
        font=("TkDefaultFont", 12, "bold"),
        bg="#ffffff",
        fg="#292421",
    ).grid(row=0, column=0, sticky="w", pady=(0, 8))

    results_text = tk.Text(
        results_frame,
        height=11,
        wrap="word",
        font=("TkDefaultFont", 10),
        bg="#ffffff",
        fg="#292421",
        relief="flat",
        borderwidth=0,
        padx=0,
        pady=0,
    )
    results_text.grid(row=1, column=0, sticky="nsew")
    results_frame.rowconfigure(1, weight=1)
    results_text.insert(
        "1.0", "Your booking details will appear here after you calculate the price."
    )
    results_text.configure(state="disabled")

    def show_results(text):
        """Replace the text shown in the booking details area."""
        results_text.configure(state="normal")
        results_text.delete("1.0", "end")
        results_text.insert("1.0", text)
        results_text.configure(state="disabled")

    def clear_form():
        """Clear both inputs and the previous booking result."""
        name_entry.delete(0, "end")
        price_entry.delete(0, "end")
        show_results("")
        name_entry.focus_set()

    def calculate_booking():
        """Validate the inputs, calculate the discount, and show the booking."""
        customer_name = name_entry.get().strip()
        price_text = price_entry.get().strip()

        if not customer_name:
            messagebox.showerror("Missing information", "Please enter the customer name.")
            name_entry.focus_set()
            return

        if not price_text:
            messagebox.showerror("Missing information", "Please enter the service price.")
            price_entry.focus_set()
            return

        try:
            original_price = float(price_text)
        except ValueError:
            messagebox.showerror("Invalid price", "Please enter a valid price.")
            price_entry.focus_set()
            return

        if not math.isfinite(original_price):
            messagebox.showerror("Invalid price", "Please enter a valid price.")
            price_entry.focus_set()
            return

        if original_price <= 0:
            messagebox.showerror("Invalid price", "Price must be a positive number.")
            price_entry.focus_set()
            return

        if original_price > DISCOUNT_LIMIT:
            discount_amount = original_price * DISCOUNT_RATE
        else:
            discount_amount = 0

        final_price = original_price - discount_amount

        show_results(
            f"Customer Name: {customer_name}\n"
            f"Original Service Price: {original_price:.2f} SAR\n"
            f"Discount Amount: {discount_amount:.2f} SAR\n"
            f"Final Price: {final_price:.2f} SAR\n\n"
            f"Congratulations {customer_name}! Your booking has been completed "
            f"successfully. The original price is {original_price:.2f} SAR, "
            f"the discount is {discount_amount:.2f} SAR, and the final price "
            f"is {final_price:.2f} SAR."
        )

    def finish():
        """Thank the employee and close the application."""
        messagebox.showinfo(
            "Thank you", "Thank you for using the Salon Booking System!"
        )
        root.destroy()

    buttons = ttk.Frame(page)
    buttons.grid(row=4, column=0, sticky="ew")
    buttons.columnconfigure(0, weight=1)
    buttons.columnconfigure(1, weight=1)

    ttk.Button(
        buttons,
        text="Calculate",
        style="Primary.TButton",
        command=calculate_booking,
    ).grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=(0, 8))
    ttk.Button(
        buttons,
        text="Add Another Customer",
        command=clear_form,
    ).grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=(0, 8))
    ttk.Button(buttons, text="Clear", command=clear_form).grid(
        row=1, column=0, sticky="ew", padx=(0, 6)
    )
    ttk.Button(buttons, text="Finish", command=finish).grid(
        row=1, column=1, sticky="ew", padx=(6, 0)
    )

    name_entry.focus_set()
    root.mainloop()


if __name__ == "__main__":
    main()
