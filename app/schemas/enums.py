from enum import Enum

class SettingCategoryEnum(str, Enum):
    general = "general"
    view = "view"
    developer = "developer"

class FolioCategoryEnum(str, Enum):
    shopping = "Shopping"
    bills_utilities = "Bills & Utilities"
    housing = "Housing"
    transportation = "Transportation"
    health_fitness = "Health & Fitness"
    entertainment = "Entertainment"
    food_drink = "Food & Drink"
    education = "Education"
    work_career = "Work & Career"
    income = "Income"
    financial_services = "Financial Services"
    gifts_donations = "Gifts & Donations"
    travel = "Travel"
    pets = "Pets"
    home_services = "Home Services"
    government_tax = "Government & Tax"
    insurance = "Insurance"
    investments = "Investments"
