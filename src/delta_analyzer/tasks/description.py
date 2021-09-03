def get_description_by(framework_occurrences, has_pytest_reference, has_unittest_reference):
  if has_pytest_reference and has_unittest_reference:
    # Now is "ongoing". Started with pytest or unittest?
    pytest_before_unittest = framework_occurrences['first_unittest']['index'] > framework_occurrences['first_pytest']['index']
    return "p => p + u" if pytest_before_unittest else "u => p + u" 

  elif has_pytest_reference:
    # Now is "pytest". Could be "migrated", "pytest only", or other migration, or something weird happened at some point
    pytest_only = not framework_occurrences['first_unittest']['hash']
    if pytest_only:
      return "p => p"
    
    pytest_before_unittest = framework_occurrences['first_unittest']['index'] > framework_occurrences['first_pytest']['index']
    return "p => (p+u or u) => p" if pytest_before_unittest else "u => p"

  elif has_unittest_reference:
    # Now is "unittest". Could be "unittest only", did the revert migration, or other migration, or something weird happened at some point
    unittest_only = not framework_occurrences['first_pytest']['hash']
    if unittest_only:
      return "u => u"
    
    pytest_before_unittest = framework_occurrences['first_unittest']['index'] > framework_occurrences['first_pytest']['index']
    return "p => u" if pytest_before_unittest else "u => (p+u or p) => u "
  elif __had_unittest_reference_before_pytest(framework_occurrences):
    return "u => ??"
  elif __had_pytest_reference_before_unittest(framework_occurrences):
    return "p => ??"
  else:
    return "unknown"

def __had_unittest_reference_before_pytest(framework_occurrences):
  if framework_occurrences['first_unittest']['hash'] != None and framework_occurrences['first_pytest']['hash'] == None:
    return True
  
  if framework_occurrences['first_unittest']['hash'] != None and framework_occurrences['first_pytest']['hash'] != None and\
      (framework_occurrences['first_unittest']['index'] < framework_occurrences['first_pytest']['index']):
    return True
  
  return False

def __had_pytest_reference_before_unittest(framework_occurrences):
  if framework_occurrences['first_pytest']['hash'] != None and framework_occurrences['first_unittest']['hash'] == None:
    return True
  
  if framework_occurrences['first_unittest']['hash'] != None and framework_occurrences['first_pytest']['hash'] != None and\
      (framework_occurrences['first_pytest']['index'] < framework_occurrences['first_unittest']['index']):
    return True
  
  return False
