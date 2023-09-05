import re

class MajorityExpression :
    
    # Cnstructor for the MajorityExpression class which takes a boolean expression string generated by the BooleanExpression class
    def __init__(self, boolean_expression):
        self.boolean_expression = boolean_expression
        
        
    #code that creates the initial majority gate logic representation of the boolean expression
    def generate_majority(self):
        
        new_expression = self.boolean_expression.replace(" AND ", "0") # replaces AND gates in the string with 0's for use in conversion to majority logic
        new_expression = new_expression.replace(" OR ", "1") # replaces OR gates in the string with 1's for use in conversion to majority logic
        
        # replaces the bar variables eg "A'" with lower case version of the same letter to represent 0 for that variable
        # This is to make the string easier to work with when converting to majority logic
        string = ''
        i = 0
        while i < len(new_expression):
            if new_expression[i].isupper() and i < len(new_expression) - 1 and new_expression[i+1] == "'":
                string += new_expression[i].lower()
                i += 2
            else:
                string += new_expression[i]
                i += 1
                
        print(string)
        
        # split the string into its majority gate groups as a list
        majority_sets = []  # Create a new list to store updated majority sets

        for i, char in enumerate(string):
            if char == '0' and string[i-1] != "⟩":
                new_string = string[slice(i-1, i+2)]
                string = string.replace(new_string, "")  # Update the string without modifying the original
                majority_sets.append(f"{new_string}")

            if char == '0' and string[i-1] == "⟩":
                new_string = string[slice(i, i+2)]
                string = string.replace(new_string, "")
                majority_sets.append(f"{new_string}")

            if char == '1' and (i == 0 or string[i-1] != '1'):
                new_string = string[slice(i, i+1)]
                string = string.replace(new_string, "")
                majority_sets.append(f"{new_string}")
                
        one_count = 0
        zero_count = 0
                
        #checks the length of the majority gate strings in the list right to left and for AND/OR gates represented by 0 and 1
        #If there are more than 3 majority gate strings two AND gates are concatenated
        if len(majority_sets) > 3 :
            for i in range(len(majority_sets) - 1, -1, -1):
                if len(majority_sets) > 3 and majority_sets[i][0] == majority_sets[i-1][-1]:
                    majority_sets[i-1] = "⟨⟨" + majority_sets[i-1] + "⟩" + majority_sets[i][1:] + "⟩"
                    majority_sets.pop(i)
        
        #brackets are added to each AND gate (0) to macth correct majority gate notation
        for i in range(len(majority_sets) - 1, -1, -1):
            
            one_count += majority_sets[i].count("1")
            zero_count += majority_sets[i].count("0")
            
            if len(majority_sets[i]) == 3 and "0" in majority_sets[i]:
                majority_sets[i] = "⟨" + majority_sets[i] + "⟩"
                
        #checks for OR gate (1) and formats it to form a complementary majority gate
        if one_count == 1 and len(majority_sets) == 3 :
            for i in range(len(majority_sets) - 1, -1, -1):
                if majority_sets[i] == "1" :
                    majority_sets.pop(i)
                    majority_sets.insert(0, "1") #used to be placed at 0, change back if problems occur
                    one_count += one_count - 1
        
        #checks for OR gate (1) and formats it to form a complementary majority gate
        if one_count >= 2 and len(majority_sets) >= 5 and len(majority_sets) > 3 :
            for i in range(len(majority_sets) - 1, -1, -1):
                if majority_sets[i] == "1" :
                    new_or_group = f"⟨{''.join(majority_sets[i-1]) if i-1 >= 0 else ''}{''.join(majority_sets[i])}{''.join(majority_sets[i+1]) if i+1 < len(majority_sets) else ''}⟩"
                    majority_sets[i] = new_or_group
                    majority_sets.pop(i - 1)
                    majority_sets.pop(i + 1)
                    one_count += one_count - 1
                    
        final_majority = f"⟨{''.join(majority_sets)}⟩"
        
        # Define the regular expression pattern to match lowercase letters
        pattern = r'[a-z]'

        # Use a lambda function as the replacement to convert lowercase letter to uppercase followed by a dot
        replacement = lambda match: match.group().upper() + "'"

        # Apply the replacement using re.sub
        final_majority_formula = re.sub(pattern, replacement, final_majority)
                    
        print("majority set sections: ", majority_sets)
                    
        return [final_majority_formula], [final_majority]

# Example usage
expression = "A' AND B' AND C AND D' OR A AND C' OR A' AND B AND D"
majority_expr = MajorityExpression(expression)
result = majority_expr.generate_majority()
print(result)