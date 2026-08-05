import { booking } from "../data/mock";

export default function BookingCard() {
    const fields = [
        ["Pickup", booking.pickup],
        ["Destination", booking.destination],
        ["Truck", booking.truck_type],
        ["Goods", booking.goods],
        ["Weight", booking.weight],
        ["Date", booking.pickup_date],
        ["Time", booking.pickup_time],
        ["Contact", booking.contact_name],
        ["Phone", booking.phone_number],
    ];

    return (
        <div className="space-y-4">
            {fields.map(([label, value]) => (
                <div
                    key={label}
                    className="flex justify-between border-b border-zinc-800 pb-2"
                >
                    <span className="text-zinc-400">
                        {label}
                    </span>

                    <span>
                        {value ?? "—"}
                    </span>
                </div>
            ))}
        </div>
    );
}