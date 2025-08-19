Location
    Address: Physical address of the charging station.
    City & Country: Where the station is located.
    Coordinates: Latitude and longitude for mapping.
    Postal Code: Local postal code.
    Operator: Company managing the station (e.g., EVB, ACV, PPEV).

EVES
    ID/UID: Unique identifier for each charging point.
    Status:
        AVAILABLE (ready to use),
        CHARGING (in use),
        UNKNOWN (status not reported),
        OUTOFORDER (not working).
    Connectors:
        Type: Socket or cable (e.g., IEC_62196_T2 for Type 2, CHADEMO for fast DC).
        Power:
            Max Power (kW): e.g., 7 kW (AC), 50 kW (DC).
            Voltage/Amperage: e.g., 230V/32A (AC), 400V/125A (DC).
    Payment: Some support RFID, credit cards, or remote start/stop.

Accessibility
    24/7 Access: Many stations are open all day ("twentyfourseven": true).
    Parking Restrictions: Mostly null (no restrictions reported).

Last Updated
    Timestamps show when the station data was last refreshed (e.g., 2024-07-10).
