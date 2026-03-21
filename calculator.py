# Math Function, calculation for sens to cm360
def sensitivity_to_cm360(sensitivity, yaw, dpi):
    
# Math Function, calculation for cm360
    counts_per_360 = 360 / (yaw * sensitivity)
    inches_per_360 = counts_per_360 / dpi
    cm_per_360 = inches_per_360 * 2.54

    result = cm_per_360
    return result
c360 = sensitivity_to_cm360(1.0, 0.022, 1600)
print(f"cm per 360: {c360:.2f}")

#Math Function, calculation for cm360 to sens
def cm360_to_sensitivity(cm360, yaw, dpi):

    inches360 = cm360/ 2.54
    counts360 = inches360 * dpi
    sensitivity = 360 / (counts360 * yaw)

    result = sensitivity
    return result
sens = cm360_to_sensitivity(c360, 0.022, 1600)
print(f"sensitivity: {sens:.2f}")

