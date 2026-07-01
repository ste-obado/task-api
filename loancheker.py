print("+++++++++++ Welcome to the Pension Checker +++++++++++++++")

age =int(input("enter you age:")) 
work_experience =int(input("enter your work experience in years:")) 
employee_type =input("enter your employee type government/private(govt/prvt):")
salary =int(input("enter your salary:"))

def gorverment_pension(employee_type, age, work_experience, salary):
  if  employee_type == "govt" and age >= 60 and work_experience >= 25 and salary >= 50000:
    pension = salary * 0.7
    print(f"Tier 1 Government Pension Approved: {pension}") 
  elif employee_type == "govt" and age >= 55 and work_experience >= 15 and salary >= 30000:
    pension = salary * 0.5
    print(f"Tier 2 Government Pension Approved: {pension}")
  else :
    print("Sorry, you do not qualify for a government pension.")

def private_pension(employee_type, age, work_experience, salary):
  if employee_type == "prvt" and age >= 60 and work_experience >= 25 and salary >= 50000:
    pension = salary * 0.6
    print(f"Tier 1 Private Pension Approved: {pension}")
  elif employee_type == "prvt" and age >= 55 and work_experience >= 15 and salary >= 30000:
    pension = salary * 0.4
    print(f"Tier 2 Private Pension Approved: {pension}")
  else:
    print("Sorry, you do not qualify for a private pension.")

def main():
    
    if employee_type == "govt":
        gorverment_pension(employee_type,age, work_experience, salary)
    elif employee_type == "prvt":
        private_pension(employee_type,age, work_experience, salary)
    else:
        print("Invalid employee type. Please enter 'govt' or 'prvt'.")

if __name__ == "__main__":

    main()