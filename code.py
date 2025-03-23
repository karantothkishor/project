import datetime
import random
import pandas as pd

# Constants
default_inflation_rate = 0.06  # 6% per annum
default_max_work_years = 40  # Maximum allowed working years
default_gross_salary = 10000  # Average base monthly salary

def generate_population_data(num_records=100):
    """Generate sample population data with random attributes."""
    population = []
    start_date = datetime.date(1960, 1, 1)
    end_date = datetime.date(2004, 12, 31)
    
    for i in range(num_records):
        dob = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
        age_years = (datetime.date(2025, 1, 1) - dob).days // 365
        age_months = ((datetime.date(2025, 1, 1) - dob).days % 365) // 30
        gender = random.choice(['Male', 'Female'])
        gross_salary = random.randint(8000, 15000)  # Monthly salary
        population.append((i + 1, gender, dob, age_years, age_months, gross_salary))
    
    return pd.DataFrame(population, columns=['ID', 'Gender', 'DOB', 'Age_Years', 'Age_Months', 'Gross_Salary'])

def build_projections(start_age, end_age, max_work_years, inflation_rate):
    """Build projected earnings for all age-month and work-month combinations."""
    projections = {}
    
    for age_years in range(start_age, end_age + 1):
        for age_months in range(0, 12):
            age_in_months = age_years * 12 + age_months
            remaining_months = max(0, min(max_work_years * 12, (60 * 12) - age_in_months))
            
            projections[(age_years, age_months)] = []
            
            for month in range(remaining_months):
                monthly_earnings = default_gross_salary * ((1 + inflation_rate / 12) ** month)
                expenditure_rate = random.uniform(0.5, 0.7)  # 50-70% of earnings
                savings_rate = random.uniform(0.1, 0.3)  # 10-30% of earnings
                investment_rate = 1 - (expenditure_rate + savings_rate)
                projections[(age_years, age_months)].append(
                    (monthly_earnings, inflation_rate, expenditure_rate, savings_rate, investment_rate)
                )
    return projections

def calculate_total_projected_earnings(population, projections):
    """Calculate total projected earnings per year for the population."""
    total_earnings = {}
    
    for _, row in population.iterrows():
        age_tuple = (row['Age_Years'], row['Age_Months'])
        if age_tuple in projections:
            yearly_earnings = sum([entry[0] for entry in projections[age_tuple]])
            total_earnings[row['ID']] = yearly_earnings
    
    return total_earnings

def get_individual_projection(projections, person_id, population):
    """Retrieve projected gross earnings for a given ID."""
    person = population[population['ID'] == person_id]
    if person.empty:
        return "ID not found."
    
    age_tuple = (person.iloc[0]['Age_Years'], person.iloc[0]['Age_Months'])
    if age_tuple in projections:
        return sum([entry[0] for entry in projections[age_tuple]])
    else:
        return "No projection available."

def get_critical_values(projections, age_years, age_months):
    """Retrieve critical values for a given age-month and projected work-month."""
    age_tuple = (age_years, age_months)
    return projections.get(age_tuple, "No data available")

if __name__ == "__main__":
    population_data = generate_population_data()
    print("Generated Population Data:")
    print(population_data.head())
    
    # User Inputs
    start_age = int(input("Enter start age: "))
    end_age = int(input("Enter end age: "))
    max_work_years = int(input("Enter max work years: "))
    inflation_rate = float(input("Enter inflation rate (decimal): "))
    
    # Building projections
    projections = build_projections(start_age, end_age, max_work_years, inflation_rate)
    
    # Total projected earnings summary
    total_earnings = calculate_total_projected_earnings(population_data, projections)
    print("Total projected earnings summary:")
    print(pd.DataFrame(total_earnings.items(), columns=['ID', 'Projected Earnings']))
    
    # Retrieve projected earnings for an ID
    person_id = int(input("Enter ID to retrieve projected earnings: "))
    print("Projected earnings for ID", person_id, ":", get_individual_projection(projections, person_id, population_data))
    
    # Retrieve critical values for a given age-month
    age_y = int(input("Enter age years to retrieve critical values: "))
    age_m = int(input("Enter age months to retrieve critical values: "))
    print("Critical values for age-month:", get_critical_values(projections, age_y, age_m))
