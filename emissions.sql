-- Trophies Table
CREATE TABLE
IF NOT EXISTS Trophies
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Weight REAL NOT NULL,
    Emission REAL NOT NULL
);

-- Momentoes Table
CREATE TABLE
IF NOT EXISTS Momentoes
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Weight REAL NOT NULL,
    Emission REAL NOT NULL
);

-- Banners Table
CREATE TABLE
IF NOT EXISTS Banners
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Weight REAL NOT NULL,
    Emission REAL NOT NULL
);

--pet water Bottle Table
CREATE TABLE
IF NOT EXISTS PetWaterBottle
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Quantity REAL NOT NULL,
    Emission REAL NOT NULL
);

CREATE TABLE
IF NOT EXISTS Kit
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Quantity REAL NOT NULL,
    Weight REAL NOT NULL,
    Emission REAL NOT NULL
);

CREATE TABLE
IF NOT EXISTS Kitems
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Quantity REAL NOT NULL,
    Weight REAL NOT NULL,
    Emission REAL NOT NULL,
    Category TEXT NOT NULL
);


-- Transport Emissions Table
CREATE TABLE
IF NOT EXISTS TransportEmissions
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Mode TEXT NOT NULL,
    Vehicle TEXT NOT NULL,
    WeightOrDistance REAL NOT NULL,
    Emission REAL NOT NULL
);

-- Electric Vehicles Consumption Table
CREATE TABLE
IF NOT EXISTS ElectricConsumption
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Vehicle TEXT NOT NULL,
    ConsumptionPerKm REAL NOT NULL  -- kWh per km
);

-- Electricity Emissions Table
CREATE TABLE
IF NOT EXISTS ElectricityEmissions
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Usage TEXT NOT NULL,         -- Type of electricity use (e.g., Lighting, Cooling, Heating)
    Value REAL NOT NULL,         -- Consumption in kWh
    Emission REAL NOT NULL       -- Emissions in kg CO₂
);

-- HVAC Emissions Table
CREATE TABLE
IF NOT EXISTS HVACEmissions
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Refrigerant TEXT NOT NULL,
    MassLeak REAL NOT NULL,
    Emission REAL NOT NULL
);

-- Food Emissions Table
CREATE TABLE
IF NOT EXISTS FoodEmissions
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    FoodItem TEXT NOT NULL,
    Quantity REAL NOT NULL,      -- Quantity in kg
    Emission REAL NOT NULL       -- Emissions in kg CO₂
);
