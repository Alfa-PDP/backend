from datetime import date
from uuid import UUID

idp_ids = [
    UUID("25a53383-5c91-442b-86f9-0cffd551fae4"),
    UUID("2bc687cb-dd90-4bd7-b9e4-6d1f80321ce9"),
    UUID("39c40fa3-891b-42c5-b8da-8996aa9e6376"),
    UUID("e4e886b5-64cb-4076-81bf-472c5351a88c"),
    UUID("9d07524e-f361-4536-8da5-c6116ef45915"),
    UUID("36e9cf6a-9cf8-402d-a2df-35653f7bc418"),
    UUID("0a1d94c5-942b-4825-bf16-345646c4857d"),
    UUID("8cd97188-6ebd-4e16-863f-05207431fc38"),
    UUID("2a949d61-f1b2-45b2-bb13-a5e0ae038150"),
    UUID("aeddb955-bcd9-4cb5-b11c-8533bf1ff135"),
]

idp_dates = [
    (date(2024, 1, 1), date(2024, 12, 31), 2024),  # start date, end date, year
    (date(2024, 1, 1), date(2024, 12, 31), 2024),
    (date(2024, 1, 1), date(2024, 12, 31), 2024),
    (date(2023, 1, 1), date(2023, 12, 31), 2023),
    (date(2023, 1, 1), date(2023, 12, 31), 2023),
    (date(2023, 1, 1), date(2023, 12, 31), 2023),
    (date(2022, 1, 1), date(2022, 12, 31), 2022),
    (date(2022, 1, 1), date(2022, 12, 31), 2022),
    (date(2022, 1, 1), date(2022, 12, 31), 2022),
    (date(2022, 1, 1), date(2022, 12, 31), 2022),
]


user_ids = [
    UUID("4a00f723-f391-4038-8d44-b48240c7e49e"),
    UUID("fde4c6dd-dd05-4295-b647-d1741d038865"),
    UUID("1d5b1f66-5534-458e-bf71-e11a9cf78cbc"),
    UUID("58158aad-9782-4752-9ad8-303c35e6a08f"),
    UUID("c19fbd26-c9f5-40a4-b897-0237670fd6e1"),
    UUID("c0390588-4e38-4c63-a216-6c6a568ce6a4"),
    UUID("27db4cc1-8250-4510-80f4-74071ffba478"),
    UUID("4baedc9d-dce8-4d18-b1c1-01a1f210ad5b"),
    UUID("5ff0565c-b5c8-4aaf-a7d6-d954a414e1bc"),
    UUID("0c0a9afb-b7b9-4271-a433-a6507166cda7"),
]


status_ids = [
    UUID("0e4aa0c9-b20c-4556-ad00-bf73e0fdf11a"),
    UUID("c11c2301-5570-4bc2-b7aa-ee0b267db522"),
    UUID("8301281d-828f-4729-a3c7-f5ba3e5121ee"),
]


team_ids = [
    UUID("52b39186-47bd-4ada-b144-b55ea3744dbf"),
    UUID("e5ea3c39-0310-4217-8bad-3807bb959a9b"),
]

leader_ids = [
    user_ids[0],
    user_ids[5],
]


task_ids = [
    UUID("09018dc5-a11d-470a-9b02-2a880f9200af"),
    UUID("76aa0eda-7748-48ce-8d99-6bb288ab4075"),
    UUID("b617a54d-57fc-42a6-84b7-85edfcf7d6f2"),
    UUID("1bc54d3a-3a21-4174-8173-bf7b8cb7e95e"),
    UUID("d9a18f01-4862-4078-ace4-735142736285"),
    UUID("9d6518aa-c34f-4444-a207-5897f911b428"),
    UUID("b0a75213-eb1f-478b-b88e-de383e355ef8"),
    UUID("fe31369b-852c-4a68-96aa-85194ab33780"),
    UUID("d4499726-39b5-43ff-96dc-771e3e81646a"),
    UUID("83ae5502-80f5-44f5-b5b5-f44fc5bdfbe0"),
    UUID("3d842b12-bbf0-4195-95fd-2309a2eb549e"),
    UUID("2d81b1bc-7acb-490f-a684-ee137a3c93ff"),
    UUID("e9b96a51-8eac-4cd0-b73c-18419544f6f4"),
    UUID("1fcb8439-7cc4-49fc-b3d5-3088c266020e"),
    UUID("84d18fe1-3b4c-426b-9953-2fb1c5127da6"),
    UUID("e244a92a-884f-4516-a9b6-2d36c385cf76"),
    UUID("020f336d-adab-4dd0-bc8d-28603fe61351"),
    UUID("7f8235ef-1c69-4d70-9669-185df5530270"),
    UUID("d11af843-c0ec-4ef4-bf35-31fb986eb907"),
    UUID("a54f36f4-8042-4d7b-b715-b705af328173"),
    UUID("b010d8c0-8ec2-40b7-9187-5449eaed544f"),
    UUID("6dc320bc-c731-4518-86a3-f21719aa8cde"),
    UUID("df30f256-d0dd-4dea-a23c-36d33a6f9fe2"),
    UUID("897896a5-ae0d-404e-af44-4eb92d4e085c"),
    UUID("277de5b8-76dd-42cc-ae3d-e75d0df67d50"),
    UUID("01840bdf-951f-406e-a540-5f39d0fde2cf"),
    UUID("9c0a4389-23f8-4a33-bb1b-d5f559861b91"),
    UUID("23efd675-4ce5-4f5a-a914-dd3a9675a32b"),
    UUID("f621ef74-f086-4f29-a49a-d49f327c0b72"),
    UUID("c1325b0c-f775-4d8f-b4d1-45748ccf0023"),
]


task_dates = [
    (date(2024, 1, 1), date(2024, 1, 31)),
    (date(2024, 2, 1), date(2024, 5, 31)),
    (date(2024, 6, 1), date(2024, 12, 31)),
    (date(2023, 1, 1), date(2023, 1, 31)),
    (date(2023, 2, 1), date(2023, 5, 31)),
    (date(2023, 6, 1), date(2023, 12, 31)),
    (date(2022, 1, 1), date(2022, 1, 31)),
    (date(2022, 2, 1), date(2022, 5, 31)),
    (date(2022, 6, 1), date(2022, 8, 31)),
    (date(2022, 8, 1), date(2022, 12, 31)),
]
