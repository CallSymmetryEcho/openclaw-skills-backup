#!/bin/bash
# Test script for project manager

echo "Testing Project Manager Tool..."
echo ""

# Test 1: Create a minimal project
echo "=== Test 1: Create minimal project ==="
./project-manager.sh create test-minimal "A test minimal project"
echo ""

# Test 2: Create a Python project
echo "=== Test 2: Create Python project ==="
./project-manager.sh create test-python "A test Python project" --template python
echo ""

# Test 3: Create a data science project
echo "=== Test 3: Create data science project ==="
./project-manager.sh create test-data "A test data science project" --template data
echo ""

# Test 4: List projects
echo "=== Test 4: List all projects ==="
./project-manager.sh list
echo ""

# Test 5: List with details
echo "=== Test 5: List projects with details ==="
./project-manager.sh list --details
echo ""

# Test 6: Open a project
echo "=== Test 6: Open a project ==="
./project-manager.sh open test-minimal
echo ""

echo "=== All tests completed ==="
echo ""
echo "Projects created in: ~/.openclaw/workspace/projects/"
echo "To clean up test projects:"
echo "  rm -rf ~/.openclaw/workspace/projects/test-*"