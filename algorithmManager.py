
class AlgorithmManager:
    pass

# Lookup table format: "<current_state>_<input_char>" -> "<next_state>"
transitions = {
    # q0 transitions
    "q0_0": "q_indiv",
    "q0_1": "q_delegate",
    
    # q_indiv transitions
    "q_indiv_0": "q_indiv_Urg",
    "q_indiv_1": "q_indiv_notUrg",
    
    # q_indiv_Urg transitions
    "q_indiv_Urg_0": "q_indiv_Urg_notImportant",
    "q_indiv_Urg_1": "q_indiv_Urg_Important",
    
    # q_indiv_notUrg transitions
    "q_indiv_notUrg_0": "q_indiv_notUrg_notImportant",
    "q_indiv_notUrg_1": "q_indiv_notUrg_Important",
    
    # q_indiv_Urg_Important transitions (inputs 1, 2, 3, 4)
    "q_indiv_Urg_Important_1": "q_doNowHigh",
    "q_indiv_Urg_Important_2": "q_doNowHigh",
    "q_indiv_Urg_Important_3": "q_doNowHigh",
    "q_indiv_Urg_Important_4": "q_doNowHigh",
    
    # q_indiv_Urg_notImportant transitions
    "q_indiv_Urg_notImportant_1": "q_doNowLow",
    "q_indiv_Urg_notImportant_2": "q_delegate",
    "q_indiv_Urg_notImportant_3": "q_delegate",
    "q_indiv_Urg_notImportant_4": "q_delegate",
    
    # q_indiv_notUrg_Important transitions
    "q_indiv_notUrg_Important_1": "q_doNowLow",
    "q_indiv_notUrg_Important_2": "q_schedule",
    "q_indiv_notUrg_Important_3": "q_canProcrastinate",
    "q_indiv_notUrg_Important_4": "q_canProcrastinate",
    
    # q_indiv_notUrg_notImportant transitions (inputs 1, 2, 3, 4)
    "q_indiv_notUrg_notImportant_1": "q_canProcrastinate",
    "q_indiv_notUrg_notImportant_2": "q_canProcrastinate",
    "q_indiv_notUrg_notImportant_3": "q_canProcrastinate",
    "q_indiv_notUrg_notImportant_4": "q_canProcrastinate",
}

def process_state_machine(inputs):
    """
    Processes a sequence of inputs through the lookup table.
    Self-loops are ignored (if key is missing, state stays the same).
    """
    current_state = "q0"
    
    for inp in inputs:
        # Concatenate current state and read input
        key = f"{current_state}_{inp}"
        
        # Look up transition
        if key in transitions:
            next_state = transitions[key]
            print(f"Input '{inp}': {current_state} --> {next_state}")
            current_state = next_state
        else:
            # Self-loops or unrecognized transitions stay in the same state
            print(f"Input '{inp}': {current_state} --> {current_state} (Self-loop/Ignored)")

    return current_state

# --- Example Run ---
# Input order: [Group?, Deadline?, Impact?, Mood]
# Example: Not group (0), Urgent (0), Important (1), Motivated (1)
input_sequence = ["0", "0", "1", "1"] 

final_state = process_state_machine(input_sequence)
print(f"\nFinal Action State: {final_state}")

    
