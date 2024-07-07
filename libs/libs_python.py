import pkg_resources

# Get a list of installed packages
installed_packages = sorted(["%s" % (i.key) for i in pkg_resources.working_set])

print(installed_packages)

with open ("libs//libs_python.txt", 'w') as file:
    for package in installed_packages:
        file.write(package + '\n')
