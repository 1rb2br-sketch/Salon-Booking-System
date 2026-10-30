import "./_group.css";
import "./Current.css";

export function Current() {
  return (
    <div className="salon-booking-extract">
      <main>
        <h1>Salon Booking</h1>
        <p className="intro">
          Enter the customer and service details to calculate the final price.
        </p>

        <form noValidate onSubmit={(event) => event.preventDefault()}>
          <label htmlFor="current-customer-name">Customer name</label>
          <input
            id="current-customer-name"
            name="customer_name"
            type="text"
            autoComplete="name"
            autoFocus
          />

          <label htmlFor="current-service-price">Service price (SAR)</label>
          <input
            id="current-service-price"
            name="price"
            type="text"
            inputMode="decimal"
            placeholder="0.00"
          />

          <div className="buttons">
            <button className="primary" type="submit" name="action" value="calculate">
              Calculate
            </button>
            <button type="submit" name="action" value="add_another">
              Add Another Customer
            </button>
            <button type="submit" name="action" value="clear">
              Clear
            </button>
            <button type="submit" name="action" value="finish">
              Finish
            </button>
          </div>
        </form>

        <section className="results" aria-live="polite">
          <h2>Booking details</h2>
          <p className="result-copy">
            Your booking details will appear here after you calculate the price.
          </p>
        </section>
      </main>
    </div>
  );
}
