"""Browser-based salon booking calculator with Python handling the booking rules."""

import html
import math
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs


# Service prices above this value qualify for the discount.
DISCOUNT_LIMIT = 150
# The discount rate is 15 percent.
DISCOUNT_RATE = 0.15


PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Salon Booking System</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      color-scheme: light;
      font-family: Arial, Helvetica, sans-serif;
      color: #292421;
      background: #f7f3ef;
    }

    * { box-sizing: border-box; }

    body {
      min-height: 100vh;
      margin: 0;
      padding: 40px 18px;
      display: grid;
      place-items: center;
      background: #f7f3ef;
    }

    main {
      width: min(100%, 560px);
      padding: 32px;
      border: 1px solid #e8dfd8;
      border-radius: 18px;
      background: #fff;
      box-shadow: 0 16px 42px rgba(57, 39, 26, 0.08);
    }

    h1 {
      margin: 0;
      font-size: 28px;
      letter-spacing: -0.5px;
    }

    .intro {
      margin: 8px 0 26px;
      color: #716760;
      font-size: 14px;
      line-height: 1.5;
    }

    label {
      display: block;
      margin: 0 0 8px;
      font-size: 14px;
      font-weight: 700;
    }

    input {
      width: 100%;
      height: 46px;
      margin: 0 0 19px;
      padding: 0 13px;
      border: 1px solid #d9cec5;
      border-radius: 9px;
      background: #fff;
      color: #292421;
      font: inherit;
    }

    input:focus {
      border-color: #9a634e;
      outline: 3px solid rgba(154, 99, 78, 0.16);
    }

    .buttons {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 2px;
    }

    button {
      min-height: 44px;
      padding: 10px 12px;
      border: 1px solid #ded5ce;
      border-radius: 9px;
      background: #fff;
      color: #37302b;
      font: inherit;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
    }

    button:hover { background: #f7f3ef; }
    button:focus-visible { outline: 3px solid rgba(154, 99, 78, 0.28); }

    button.primary {
      border-color: #87543f;
      background: #87543f;
      color: #fff;
    }

    button.primary:hover { background: #714330; }

    .results {
      margin-top: 24px;
      padding: 17px;
      border: 1px solid #e8dfd8;
      border-radius: 12px;
      background: #fcfaf8;
    }

    .results h2 {
      margin: 0 0 10px;
      font-size: 16px;
    }

    .result-copy {
      margin: 0;
      color: #504841;
      font-size: 14px;
      line-height: 1.7;
      white-space: pre-line;
      overflow-wrap: anywhere;
    }

    .alert {
      margin: 0 0 18px;
      padding: 11px 12px;
      border: 1px solid #e9bdb7;
      border-radius: 8px;
      background: #fff4f2;
      color: #8b2f27;
      font-size: 14px;
    }

    @media (max-width: 480px) {
      body { padding: 18px 12px; }
      main { padding: 23px 18px; }
      h1 { font-size: 24px; }
      .buttons { grid-template-columns: 1fr; }
    }

    :root {
      color-scheme: light;
      font-family: "DM Sans", Arial, sans-serif;
      color: #49383b;
      background: #f8f0ed;
    }

    body {
      min-height: 100vh;
      padding: clamp(22px, 5vh, 52px) 18px;
      background:
        radial-gradient(ellipse at 8% 12%, rgba(231, 194, 193, 0.38), transparent 30%),
        radial-gradient(ellipse at 92% 88%, rgba(224, 205, 174, 0.28), transparent 32%),
        #f8f0ed;
    }

    main {
      position: relative;
      isolation: isolate;
      width: min(100%, 590px);
      padding: clamp(27px, 5vw, 42px);
      overflow: hidden;
      border: 1px solid rgba(180, 137, 119, 0.27);
      border-radius: 28px;
      background: rgba(255, 252, 249, 0.96);
      box-shadow:
        0 26px 70px rgba(92, 58, 61, 0.12),
        0 4px 14px rgba(92, 58, 61, 0.05);
      animation: salon-entry 680ms cubic-bezier(0.2, 0.75, 0.25, 1) both;
    }

    main::before {
      position: absolute;
      z-index: -1;
      inset: 0 16% auto;
      height: 3px;
      border-radius: 0 0 4px 4px;
      background: linear-gradient(90deg, transparent, #d7b87d 24%, #c28d91 52%, #d7b87d 78%, transparent);
      content: "";
    }

    h1 {
      display: flex;
      align-items: center;
      gap: 13px;
      color: #593b43;
      font-family: "Cormorant Garamond", Georgia, serif;
      font-size: clamp(32px, 7vw, 42px);
      font-weight: 600;
      letter-spacing: 0.01em;
      line-height: 1;
    }

    h1::before {
      width: 34px;
      height: 34px;
      flex: 0 0 34px;
      background:
        radial-gradient(ellipse 5px 9px at 50% 19%, #c5a06b 0 58%, transparent 62%),
        radial-gradient(ellipse 5px 9px at 81% 42%, #d5b788 0 58%, transparent 62%),
        radial-gradient(ellipse 5px 9px at 69% 77%, #c5a06b 0 58%, transparent 62%),
        radial-gradient(ellipse 5px 9px at 31% 77%, #d5b788 0 58%, transparent 62%),
        radial-gradient(ellipse 5px 9px at 19% 42%, #c5a06b 0 58%, transparent 62%),
        radial-gradient(circle at 50% 50%, #956a73 0 3px, transparent 3.5px);
      content: "";
    }

    .intro {
      margin: 10px 0 29px;
      color: #817276;
      font-size: 14px;
      line-height: 1.65;
    }

    label {
      margin-bottom: 9px;
      color: #76535d;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.075em;
    }

    input {
      height: 53px;
      margin-bottom: 21px;
      padding: 0 16px;
      border: 1px solid #e7d6d1;
      border-radius: 13px;
      background: #fffdfb;
      color: #49383b;
      font-size: 15px;
      transition: border-color 180ms ease, box-shadow 180ms ease, background-color 180ms ease;
    }

    input::placeholder {
      color: #b5a7a6;
    }

    input:focus {
      border-color: #b77f8a;
      outline: 3px solid rgba(183, 127, 138, 0.14);
      background: #fff;
      box-shadow: 0 5px 16px rgba(136, 84, 99, 0.08);
    }

    .buttons {
      gap: 12px;
      margin-top: 4px;
    }

    button {
      min-height: 50px;
      padding: 12px 14px;
      border: 1px solid #e7d9d4;
      border-radius: 13px;
      background: #fffdfa;
      color: #5e484d;
      font-family: inherit;
      font-size: 13px;
      font-weight: 700;
      transition:
        transform 180ms ease,
        box-shadow 180ms ease,
        background-color 180ms ease,
        border-color 180ms ease,
        color 180ms ease;
    }

    button:hover {
      transform: translateY(-2px);
      border-color: #d8b9b5;
      background: #fff8f5;
      box-shadow: 0 8px 18px rgba(100, 61, 68, 0.09);
    }

    button:active {
      transform: translateY(0) scale(0.985);
      box-shadow: none;
    }

    button:focus-visible {
      outline: 3px solid rgba(177, 123, 134, 0.28);
      outline-offset: 2px;
    }

    button.primary {
      border-color: #a66f7b;
      background: linear-gradient(135deg, #b47d88, #98616f);
      color: #fffaf8;
      box-shadow: 0 7px 17px rgba(132, 76, 91, 0.17);
    }

    button.primary:hover {
      border-color: #87515f;
      background: linear-gradient(135deg, #a36b77, #87515f);
      box-shadow: 0 10px 22px rgba(132, 76, 91, 0.22);
    }

    button[value="add_another"] {
      border-color: #ebd4d2;
      background: #fbefed;
      color: #774f59;
    }

    button[value="add_another"]:hover {
      background: #f7e4e2;
    }

    button[value="finish"] {
      border-color: #dfc995;
      background: #f8f1e3;
      color: #745c37;
    }

    button[value="finish"]:hover {
      border-color: #cbb071;
      background: #f3e9d3;
    }

    .results {
      position: relative;
      margin-top: 28px;
      padding: 21px 22px;
      border: 1px solid #e8d8c1;
      border-radius: 19px;
      background: linear-gradient(145deg, #fffaf3, #fcf4ee);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.85);
      transition: border-color 220ms ease, box-shadow 220ms ease, background 220ms ease;
    }

    .results::before {
      position: absolute;
      top: 0;
      right: 22px;
      left: 22px;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(190, 158, 102, 0.54), transparent);
      content: "";
    }

    .results h2 {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin: 0 0 10px;
      color: #65464e;
      font-family: "Cormorant Garamond", Georgia, serif;
      font-size: 22px;
      font-weight: 600;
      letter-spacing: 0.01em;
    }

    .result-copy {
      margin: 0;
      color: #6f6061;
      font-size: 13px;
      line-height: 1.75;
      white-space: pre-line;
      overflow-wrap: anywhere;
    }

    .alert {
      margin: 0 0 18px;
      padding: 12px 14px;
      border: 1px solid #e8c4c3;
      border-radius: 12px;
      background: #fff4f2;
      color: #8a4d57;
      font-size: 13px;
      line-height: 1.5;
      box-shadow: 0 4px 12px rgba(140, 79, 86, 0.06);
    }

    .results.has-success {
      border-color: #d9c08f;
      background: linear-gradient(145deg, #fffaf1, #fbf1e8);
      box-shadow: 0 10px 26px rgba(132, 99, 58, 0.08);
    }

    .success-check {
      display: inline-grid;
      width: 32px;
      height: 32px;
      flex: 0 0 32px;
      place-items: center;
      border-radius: 50%;
      background: linear-gradient(135deg, #bf9d67, #a47a48);
      box-shadow: 0 4px 10px rgba(164, 122, 72, 0.2);
      animation: check-pop 480ms cubic-bezier(0.2, 0.9, 0.3, 1.3) both;
    }

    .success-check svg {
      width: 17px;
      height: 17px;
      overflow: visible;
    }

    .success-check path {
      fill: none;
      stroke: #fff;
      stroke-linecap: round;
      stroke-linejoin: round;
      stroke-width: 2.5;
      stroke-dasharray: 22;
      stroke-dashoffset: 22;
      animation: check-draw 360ms 180ms ease-out forwards;
    }

    .result-copy .result-line {
      display: block;
      animation: value-arrive 420ms ease-out both;
    }

    .result-copy .result-spacer {
      display: block;
      height: 8px;
    }

    .result-copy .result-discount {
      color: #96616e;
      font-weight: 600;
      animation-delay: 120ms;
    }

    .result-copy .result-final {
      color: #69444e;
      font-weight: 700;
      animation-delay: 220ms;
    }

    .result-copy .result-summary {
      margin-top: 7px;
      color: #716063;
      animation-delay: 300ms;
    }

    @keyframes salon-entry {
      from { opacity: 0; transform: translateY(14px) scale(0.99); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    @keyframes check-pop {
      from { opacity: 0; transform: scale(0.58) rotate(-12deg); }
      to { opacity: 1; transform: scale(1) rotate(0); }
    }

    @keyframes check-draw {
      to { stroke-dashoffset: 0; }
    }

    @keyframes value-arrive {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 520px) {
      body { padding: 20px 12px; }
      main { padding: 27px 21px; border-radius: 23px; }
      h1 { gap: 10px; font-size: 33px; }
      h1::before { width: 29px; height: 29px; flex-basis: 29px; }
      .buttons { grid-template-columns: 1fr; gap: 9px; }
      .results { padding: 18px; }
    }

    @media (prefers-reduced-motion: reduce) {
      *,
      *::before,
      *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
      }
    }
  </style>
</head>
<body>
  <main>
    <h1>Salon Booking System</h1>
    <p class="intro">Enter the customer and service details to calculate the final price.</p>
    <!-- APP_CONTENT -->
  </main>
  <script>
    (() => {
      const results = document.querySelector(".results");
      const resultCopy = results?.querySelector(".result-copy");
      if (!results || !resultCopy) return;

      const originalText = resultCopy.textContent || "";
      if (!originalText.includes("Congratulations") || !originalText.includes("Final Price:")) return;

      results.classList.add("has-success");
      const heading = results.querySelector("h2");
      if (heading) {
        const marker = document.createElement("span");
        marker.className = "success-check";
        marker.setAttribute("aria-hidden", "true");
        marker.innerHTML = '<svg viewBox="0 0 24 24"><path d="m5 12 4 4L19 6"></path></svg>';
        heading.append(marker);
      }

      resultCopy.replaceChildren(...originalText.split("\\n").map((line) => {
        const item = document.createElement("span");
        if (!line) {
          item.className = "result-spacer";
          item.setAttribute("aria-hidden", "true");
          return item;
        }
        item.className = "result-line";
        if (line.startsWith("Discount Amount:")) item.classList.add("result-discount");
        if (line.startsWith("Final Price:")) item.classList.add("result-final");
        if (line.startsWith("Congratulations")) item.classList.add("result-summary");
        item.textContent = line;
        return item;
      }));
    })();
  </script>
</body>
</html>
"""


# Calculate the discount and final price, then build the booking summary.
def format_booking(customer_name, original_price):
    """Apply the salon discount rule and return the booking summary."""
    # Apply 15% only when the service price is above the discount limit.
    discount_amount = (
        original_price * DISCOUNT_RATE
        if original_price > DISCOUNT_LIMIT
        else 0
    )
    # Subtract the discount to get the amount the customer pays.
    final_price = original_price - discount_amount

    return (
        f"Customer Name: {customer_name}\n"
        f"Original Service Price: {original_price:.2f} SAR\n"
        f"Discount Amount: {discount_amount:.2f} SAR\n"
        f"Final Price: {final_price:.2f} SAR\n\n"
        f"Congratulations {customer_name}! Your booking has been completed "
        f"successfully. The original price is {original_price:.2f} SAR, "
        f"the discount is {discount_amount:.2f} SAR, and the final price "
        f"is {final_price:.2f} SAR."
    )


# Build the browser page with the form or the finished booking message.
def render_page(customer_name="", price="", error="", result="", finished=False):
    """Render the single-screen booking interface."""
    if finished:
        content = """
    <section class="results" aria-live="polite">
      <h2>Thank you</h2>
      <p class="result-copy">Thank you for using the Salon Booking System!</p>
    </section>
"""
    else:
        # Escape customer input before placing it in the page.
        safe_name = html.escape(customer_name, quote=True)
        safe_price = html.escape(price, quote=True)
        error_html = (
            f'<p class="alert" role="alert">{html.escape(error)}</p>'
            if error
            else ""
        )
        result_html = html.escape(result) if result else (
            "Your booking details will appear here after you calculate the price."
        )
        content = f"""
    <form method="post" action="/" novalidate>
      <label for="customer-name">Customer name</label>
      <input id="customer-name" name="customer_name" type="text"
             value="{safe_name}" autocomplete="name" autofocus>

      <label for="service-price">Service price (SAR)</label>
      <input id="service-price" name="price" type="text" inputmode="decimal"
             value="{safe_price}" placeholder="0.00">

      {error_html}

      <div class="buttons">
        <button class="primary" type="submit" name="action" value="calculate">Calculate</button>
        <button type="submit" name="action" value="add_another">Add Another Customer</button>
        <button type="submit" name="action" value="clear">Clear</button>
        <button type="submit" name="action" value="finish">Finish</button>
      </div>
    </form>

    <section class="results" aria-live="polite">
      <h2>Booking details</h2>
      <p class="result-copy">{result_html}</p>
    </section>
"""

    return PAGE_TEMPLATE.replace("<!-- APP_CONTENT -->", content)


class SalonBookingHandler(BaseHTTPRequestHandler):
    """Serve the browser interface and handle booking form submissions."""

    def do_GET(self):
        self.send_html(render_page())

    def do_POST(self):
        # Read and parse the values sent by the booking form.
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            form_body = self.rfile.read(content_length).decode("utf-8")
            fields = parse_qs(form_body, keep_blank_values=True)
        except (UnicodeDecodeError, ValueError):
            self.send_html(render_page(error="Please enter a valid price."))
            return

        # Find which button the customer clicked.
        action = fields.get("action", [""])[0]
        # Keep the customer name and service price as text until validation.
        customer_name = fields.get("customer_name", [""])[0].strip()
        price_text = fields.get("price", [""])[0].strip()

        if action == "finish":
            self.send_html(render_page(finished=True))
        elif action in ("clear", "add_another"):
            self.send_html(render_page())
        elif action == "calculate":
            self.calculate_and_respond(customer_name, price_text)
        else:
            self.send_html(render_page(error="Please enter a valid price."))

    # Validate the name and price before calculating the booking.
    def calculate_and_respond(self, customer_name, price_text):
        # A customer name is required.
        if not customer_name:
            self.send_html(
                render_page(
                    customer_name=customer_name,
                    price=price_text,
                    error="Please enter the customer name.",
                )
            )
            return

        # A service price is required.
        if not price_text:
            self.send_html(
                render_page(
                    customer_name=customer_name,
                    error="Please enter the service price.",
                )
            )
            return

        try:
            # Convert the entered price from text to a number.
            original_price = float(price_text)
        except ValueError:
            self.send_html(
                render_page(
                    customer_name=customer_name,
                    price=price_text,
                    error="Please enter a valid price.",
                )
            )
            return

        # Reject values that are not finite numbers, such as infinity.
        if not math.isfinite(original_price):
            self.send_html(
                render_page(
                    customer_name=customer_name,
                    price=price_text,
                    error="Please enter a valid price.",
                )
            )
            return

        # The service price must be greater than zero.
        if original_price <= 0:
            self.send_html(
                render_page(
                    customer_name=customer_name,
                    price=price_text,
                    error="Price must be a positive number.",
                )
            )
            return

        self.send_html(
            render_page(
                customer_name=customer_name,
                price=price_text,
                result=format_booking(customer_name, original_price),
            )
        )

    def send_html(self, page):
        response = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format_string, *args):
        """Keep routine requests quiet in the workflow log."""


def main():
    """Start the Replit Preview web server."""
    # Use Replit's port, or 8000 when running locally.
    port = int(os.environ.get("PORT", "8000"))
    # Connect browser requests to the booking handler.
    server = ThreadingHTTPServer(("0.0.0.0", port), SalonBookingHandler)
    print(f"Salon Booking System is listening on port {port}.")
    # Keep listening for requests; this is the server's main loop.
    server.serve_forever()


if __name__ == "__main__":
    main()
