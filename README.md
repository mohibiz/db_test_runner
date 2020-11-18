# Credits
I have used lots of resources on the web to write the code. So please let me know if you like me to add you in credits if your content is used

# Introduction 
This tool is created for automation of oracle test scripts using python's pytest framework.It's generic in nature and could be used by anyone under the tool's limitations
 
# Objective 
create a common platform to be able run existing database test scripts(or use existing database skills) and generate test report.

#Tool
test-runner v1.001

# Author
@Mohit Gupta 

# Purpose 
1. Avoid manual execution ,test output recording , error reporting of oracle test scripts hence save time , effort and manual errors
2. Bypass execution and Jump straight on analysis based on generated test output report.
3. Utilise existing  skills capability (oracle )

 
# Supported Database in current Release
Oracle , all versions supported by python's cx_Oracle module

# Planned addition
MSSQL
MySQL


# Test Framework 
Pytest

# How it works : 
1. test-runner picks up the record from control table(a csv file)  based on  execution flag then
2. Based on control record It identifies what test script is associated with test then
3. It picks up the script from configured location. Then replaces the bind variables(if any) with values defined in control file then
4. It executes the test script(sql or plsql) in configured target database then
5. After successful  execution of script test-runner run the passing criteria sql and compares it with the passing criteria then
6. Based on the outcome of comparison  test-runner generates the outputs of passed and failed tests along with detailed message of cause of failure then
7. Results of test execution can be shared for team to analyse the failed tests 

# General Feature List
1. test-runner picks up the record  from control table(csv file)  based on  execution flag then
2. Based on control record It identifies what test script is associated with test then
3. It picks up the script from configured location. Then replaces the bind variables(if any) with values defined in control file then
4. It executes the test script(sql or plsql) in configured target database then
5. After successful  execution of script test-runner run the passing criteria sql and compares it with the passing criteria then
6. Based on the outcome of comparison  test-runner generates the outputs of passed and failed tests along with detailed message of cause of failure then
7. Results of test execution can be shared for team to analyse the failed tests 
8. Detailed Logging and Reporting of test-runner , scripts and test execution


# Supported Oracle Scripts 
1. SQL File with/without bind variables (varchar ,number , dates )
2. PLSQL File with/without bind variables (varchar,number , dates )


#  Pre requisites/Dependencies
1. Python3.7.4 Or above
2. Checkout requirement.txt for python dependencies. to install, navigate to file (requirements.txt) run following command 
    ```pip install -r requirements.txt```

# Getting Started
1. Installation process
2. Activate virtual environment
3. How to use
   1. How to write test Scripts
   2. How to Run the test-runner


## Installation process
1. Clone the repository
2. Edit pyenv.cfg for python installation details or place the python libraries in following locaiton
   C:\installations\Python3.7.4   

3. you can install your own virtual environment. Make sure that you have all the packages installed listed in requirement requirements.txt
   if above mentioned python packages are not installed then run following command to install them
   pip install -r requirements.txt
   

## How to Run
    
### How to write test scripts
To be able run the test scripts , test-runner expects then to written in certain way.check out the templates in following location.
test-runner\src\main\test-scripts\oracle\*.sql and *.plsql

test script execution is controlled by control_table.csv file.This drives the dynamic generation of the tests using pytest framework. checkout the description for control file. Also checkout the template in following location 
test-runner\src\main\test-scripts\oracle\control_table.csv
  control table header | Description
  --------------------- | --------------------- 
  Jira_number | Name explains it, for informational usage . it does not have any impact on execution . Ex xyz-1
  Test_case | Name of the test case. This is  for informational usage . It does not have any impact on execution although it will be used for jira integration in future releases Ex. Sql_test1
  Script_id | Id of the test script. This is  for informational usage . It does not have any impact on execution. Ex . script1
  Script_name | Name of the test script file which requires execution . There are two types of files support. .sql and .plsql. This file name used to create tests dynamically .Ex . sqlblock1.sql 
  Resultant_sql(passing criteria sql) | This is sql statement which needs to be defined as part of the test based on the final temporary table created as part of test script (script_name) Ex . select count(*) from sql_block1
  Passing_criteria (Passing criteria value) | This should indicate the expected output of resultant_sql.  It can have single value or multiple values separated by comma. It should be match with the output of resultant_sql for test to pass Ex (25,)
  Input_variable | Variables which needs to be passed test script at run time . it can be single or multiple variables separated by comma, Ex . {'var_subcasenumber' : "'case_001'"}
  Comments | Comment related to test  , for informational usage . it does not have any impact on execution
  Execution_flag | It indicates if test needs to be executed or not . Ex . ‘Y’ or ‘N’

  

#### General Guidelines

1. Test script should have extension .sql (for SQL ) and .plsql (for PLSQL).test-runner picks of the script based on file extension and deals with them differently 
2. Mandatory fields to be defined for each test script, One final resultant table , passing criteria sql and passing criteria
3. Update script header with relevant details of the test. This is information goes in control table for execution .currently it will need to be done manually but I plan to extract this by test-runner in next release.
4. There are two ways test can be reported as failed , 
   1. test script failed to execute correctly ( process or script failure . meaning bad failure ).We don’t want this
   2. test script executed ok but resultant sql and passing criteria did not match(legit failure ).  We definitely want that so we can raise some beautiful jira’s 😃 . We do that manually Until jira integration comes in effect 
7. It’s individuals responsibility to write/test the test script in Oracle session as test-runner is just an engine. If script fails because of (syntax error , logic errors etc), test will fail as well .although logs will be available for failed tests for investigations.
8. for every test script ,there has to be a corresponding entry in control_table.csv.execution can be controlled by Execution_flag. 


### How to run test-runner
1. Make sure all the installation steps are completed.
2. place your test(.sql/.plsql) scripts in a directory.check out the format in script-examples test-runner\src\main\test-scripts\oracle\*.sql and *.plsql
3. place control file (.csv file ).check out the format in script-examples in test-runner\src\main\test-scripts\oracle\control_table.csv
4. place config file (.json file) in a directory. check out the format in test-runner\config\oracle\*.json
5. Navigate to file test-engine 
```cd test-runner\src\main\test-engine```
6. Run the following command
```run.py --script-path=<absolute path for script/scripts> --control-file=<absolute path for control file> --config-file=<absolute path for config file>```
   
   *check the Env.py file for default settings.*
    

# Known Issues
To be identified

# Contribute
Please let me know if you like to contribute.

# Support
This tools is not actively supported. 

## The end