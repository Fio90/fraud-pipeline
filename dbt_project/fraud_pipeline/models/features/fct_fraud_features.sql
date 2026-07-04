WITH base AS (
    SELECT * FROM {{ ref('stg_transactions') }}
),

features AS (
    SELECT
        -- Identifiers
        transaction_id,
        transaction_dt,
        transaction_amt,
        is_fraud,

        -- Feature 1: Address mismatch (billing vs shipping)
        CASE
            WHEN billing_address IS NULL OR shipping_address IS NULL THEN 0
            WHEN billing_address != shipping_address THEN 1
            ELSE 0
        END AS address_mismatch,

        -- Feature 2: High value transaction flag
        CASE
            WHEN transaction_amt > 500 THEN 1
            ELSE 0
        END AS high_value_transaction,

        -- Feature 3: Email domain mismatch
        CASE
            WHEN purchaser_email_domain IS NULL OR recipient_email_domain IS NULL THEN 0
            WHEN purchaser_email_domain != recipient_email_domain THEN 1
            ELSE 0
        END AS email_domain_mismatch,

        -- Feature 4: Distance risk flag
        CASE
            WHEN distance1 IS NULL THEN 0
            WHEN distance1 > 100 THEN 1
            ELSE 0
        END AS high_distance_risk,

        -- Feature 5: Card type risk
        CASE
            WHEN card6 = 'credit' THEN 1
            ELSE 0
        END AS is_credit_card,

        -- Feature 6: Mobile device flag
        CASE
            WHEN device_type = 'mobile' THEN 1
            ELSE 0
        END AS is_mobile_device,

        -- Synthetic signals
        vpn_detected,
        card_pasted,
        disposable_email,

        -- Raw columns for ML model
        card1,
        card2,
        card3,
        card4,
        card5,
        card6,
        distance1,
        distance2,
        product_cd,
        purchaser_email_domain,
        recipient_email_domain,
        device_type

    FROM base
)

SELECT * FROM features