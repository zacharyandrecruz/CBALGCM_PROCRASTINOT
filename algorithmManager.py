
class AlgorithmManager:

    transitions = {

        "q0_0": "q_indiv",
        "q0_1": "q_delegate",

        "q_indiv_0": "q_indiv_Urg",
        "q_indiv_1": "q_indiv_notUrg",

        "q_indiv_Urg_0": "q_indiv_Urg_notImportant",
        "q_indiv_Urg_1": "q_indiv_Urg_Important",

        "q_indiv_notUrg_0": "q_indiv_notUrg_notImportant",
        "q_indiv_notUrg_1": "q_indiv_notUrg_Important",

        "q_indiv_Urg_Important_1": "q_doNowHigh",
        "q_indiv_Urg_Important_2": "q_doNowHigh",
        "q_indiv_Urg_Important_3": "q_doNowHigh",
        "q_indiv_Urg_Important_4": "q_doNowHigh",

        "q_indiv_Urg_notImportant_1": "q_doNowLow",
        "q_indiv_Urg_notImportant_2": "q_delegate",
        "q_indiv_Urg_notImportant_3": "q_delegate",
        "q_indiv_Urg_notImportant_4": "q_delegate",

        "q_indiv_notUrg_Important_1": "q_doNowLow",
        "q_indiv_notUrg_Important_2": "q_schedule",
        "q_indiv_notUrg_Important_3": "q_canProcrastinate",
        "q_indiv_notUrg_Important_4": "q_canProcrastinate",

        "q_indiv_notUrg_notImportant_1": "q_canProcrastinate",
        "q_indiv_notUrg_notImportant_2": "q_canProcrastinate",
        "q_indiv_notUrg_notImportant_3": "q_canProcrastinate",
        "q_indiv_notUrg_notImportant_4": "q_canProcrastinate"

    }

    def process_state_machine_algorithm(self, inputs):

        current_state = "q0"

        for char in inputs:

            key = f"{current_state}_{char}"

            if key in self.transitions:
                current_state = self.transitions[key]
            else:
                return -1

        match(current_state):
            case "q_doNowHigh" : return 0
            case "q_doNowLow" : return 1
            case "q_schedule" : return 2
            case "q_canProcrastinate" : return 3
            case "q_delegate" : return 4

        return -1


    
