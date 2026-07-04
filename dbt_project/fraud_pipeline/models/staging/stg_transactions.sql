WITH source AS (
    SELECT * FROM raw_transactions
),

staged AS (
    SELECT
        -- Transaction identifiers
        "TransactionID"         AS transaction_id,
        "TransactionDT"         AS transaction_dt,
        "TransactionAmt"        AS transaction_amt,
        "isFraud"               AS is_fraud,

        -- Product info
        "ProductCD"             AS product_cd,

        -- Card info
        "card1"                 AS card1,
        "card2"                 AS card2,
        "card3"                 AS card3,
        "card4"                 AS card4,
        "card5"                 AS card5,
        "card6"                 AS card6,

        -- Address info
        "addr1"                 AS billing_address,
        "addr2"                 AS shipping_address,
        "dist1"                 AS distance1,
        "dist2"                 AS distance2,

        -- Email domains
        "P_emaildomain"         AS purchaser_email_domain,
        "R_emaildomain"         AS recipient_email_domain,

        -- Device info
        "DeviceType"            AS device_type,
        "DeviceInfo"            AS device_info,

        -- Synthetic fraud signals
        vpn_detected,
        card_pasted,
        disposable_email

    FROM source
    WHERE "TransactionID" IS NOT NULL
)

SELECT * FROM staged