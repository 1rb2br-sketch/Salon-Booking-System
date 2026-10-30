"""Browser-based salon booking calculator with Python handling the booking rules."""

import html
import math
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs


DISCOUNT_LIMIT = 150
DISCOUNT_RATE = 0.15


PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Salon Booking System</title>
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
  </style>
</head>
<body>
  <main>
    <h1>Salon Booking</h1>
    <p class="intro">Enter the customer and service details to calculate the final price.</p>
    <!-- APP_CONTENT -->
  </main>
</body>
</html>
"""


def format_booking(customer_name, original_price):
    """Apply the salon discount rule and return the booking summary."""
    discount_amount = (
        original_price * DISCOUNT_RATE
        if original_price > DISCOUNT_LIMIT
        else 0
    )
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
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            form_body = self.rfile.read(content_length).decode("utf-8")
            fields = parse_qs(form_body, keep_blank_values=True)
        except (UnicodeDecodeError, ValueError):
            self.send_html(render_page(error="Please enter a valid price."))
            return

        action = fields.get("action", [""])[0]
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

    def calculate_and_respond(self, customer_name, price_text):
        if not customer_name:
            self.send_html(
                render_page(
                    customer_name=customer_name,
                    price=price_text,
                    error="Please enter the customer name.",
                )
            )
            return

        if not price_text:
            self.send_html(
                render_page(
                    customer_name=customer_name,
                    error="Please enter the service price.",
                )
            )
            return

        try:
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

        if not math.isfinite(original_price):
            self.send_html(
                render_page(
                    customer_name=customer_name,
                    price=price_text,
                    error="Please enter a valid price.",
                )
            )
            return

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
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), SalonBookingHandler)
    print(f"Salon Booking System is listening on port {port}.")
    server.serve_forever()


if __name__ == "__main__":
    main()
