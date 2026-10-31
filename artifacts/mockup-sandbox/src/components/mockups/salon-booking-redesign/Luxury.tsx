import "./_group.css";
import "./Luxury.css";

export function Luxury() {
  return (
    <div className="salon-booking-extract salon-booking-luxury">
      <main>
        <p className="eyebrow" aria-hidden="true">Salon appointment desk</p>
        <h1>Salon Booking System</h1>
        <p className="intro">
          Enter the customer and service details to calculate the final price.
        </p>

        <form noValidate onSubmit={(event) => event.preventDefault()}>
          <label htmlFor="luxury-customer-name">Customer name</label>
          <input
            id="luxury-customer-name"
            name="customer_name"
            type="text"
            autoComplete="name"
            autoFocus
          />

          <label htmlFor="luxury-service-price">Service price (SAR)</label>
          <input
            id="luxury-service-price"
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
          <div className="result-heading">
            <h2>Booking details</h2>
          </div>
          <p className="result-copy">
            Your booking details will appear here after you calculate the price.
          </p>
        </section>
      </main>
    </div>
  );
}
