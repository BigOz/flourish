# flourish
Simulates energy usage of various combinations of technologies. Intendeded to help consumers understand what kind of savings they can expect from investing in technologies.

### Running Simulator
An example script demonstrates how to start and run the program. There are several flags that must be set by the user, which are explained in the script.

Currently, for the program to work, there need to be two binary files present, "2016_solar_actual" and "2016_solar_predictions". These binary files are pickled 2D 366 X 24 arrays, representing solar predictions and actual values for all of 2016. If a user wishes to use their own files, they simply need a similar pickled array, where each value represents the wattage available from solar panels at any hour of a year.

### Output
The program will output a CSV file with appropriate data. The filename is automatically constructed based on the flags used to launch the program

### Modifications
A user may choose to implement their own smart battery objects. There is simply a battery class with only a single function, "get move". If you inherit from this class, you can implement your own smart battery. There is an "evaluator" object that you can pass to your smart battery upon creation, if necessary. This evaluator allows the battery to have access to predictions and to understand the ramifications of making a specific choice, without risk of accidentally modifying the current state.

There are also various "predictors" that one might choose to further implement. They currently rely on basic algorithms and lists to get values, but more robust implementations are possible that take into consideration time of year, etc.

### Data
Much of the data for this project was used only with permission. Therefore, the data contained in this repository is everything I am permitted to share unconditionally at this time.
