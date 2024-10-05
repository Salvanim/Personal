class ClassFactory:
    def __init__(self):
        self._registry = {}
        self._variables = {}

    def create_class(self, class_name, base_classes=(), class_attributes=None):
        if class_attributes is None:
            class_attributes = {}

        if class_name in self._registry:
            raise ValueError(f"A class named '{class_name}' already exists in the registry.")

        new_class = type(class_name, base_classes, class_attributes)
        self._registry[class_name] = new_class
        return new_class

    def get_class(self, class_name):
        try:
            return self._registry[class_name]
        except KeyError:
            raise KeyError(f"No class named '{class_name}' found in the registry.")

    def list_classes(self):
        return list(self._registry.keys())

    def overwrite_method(self, class_name, method_name, new_method):
        cls = self.get_class(class_name)
        if not hasattr(cls, method_name):
            raise AttributeError(f"The class '{class_name}' does not have a method named '{method_name}' to overwrite.")
        setattr(cls, method_name, new_method)

    def add_attribute(self, class_name, attribute_name, value):
        cls = self.get_class(class_name)
        setattr(cls, attribute_name, value)

    def remove_class(self, class_name):
        try:
            del self._registry[class_name]
        except KeyError:
            raise KeyError(f"No class named '{class_name}' found in the registry to remove.")

    def clear_registry(self):
        self._registry.clear()

    def add_variable(self, var_name, value):
        self._variables[var_name] = value
        super().__setattr__(var_name, value)

    def get_variable(self, var_name):
        try:
            return self._variables[var_name]
        except KeyError:
            raise KeyError(f"No variable named '{var_name}' found in the factory.")

    def list_variables(self):
        return list(self._variables.keys())

    def remove_variable(self, var_name):
        try:
            del self._variables[var_name]
            delattr(self, var_name)
        except KeyError:
            raise KeyError(f"No variable named '{var_name}' found in the factory to remove.")
        except AttributeError:
            raise AttributeError(f"Attribute '{var_name}' does not exist on the factory.")

    def __getattr__(self, name):
        if name in self._registry:
            return self._registry[name]
        elif name in self._variables:
            return self._variables[name]
        else:
            raise AttributeError(f"'ClassFactory' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        elif name in self._registry:
            self._registry[name] = value
        else:
            self._variables[name] = value
            super().__setattr__(name, value)


# Example Usage
if __name__ == "__main__":
    # Initialize the factory
    factory = ClassFactory()

    # Create ClassA
    attributes_a = {
        'greet': lambda self: f"Hello from {self.__class__.__name__}!",
        'attribute_a': 100
    }
    ClassA = factory.create_class('ClassA', (), attributes_a)

    # Create ClassB
    def custom_greet(self):
        return f"Greetings from {self.__class__.__name__}!"

    attributes_b = {
        'greet': custom_greet,
        'attribute_b': 'Python Dynamic Class'
    }
    ClassB = factory.create_class('ClassB', (), attributes_b)

    # List classes
    print("Classes in registry:", factory.list_classes())  # ['ClassA', 'ClassB']

    # Instantiate and use ClassA
    instance_a = factory.ClassA()
    print(instance_a.greet())         # Hello from ClassA!
    print(instance_a.attribute_a)     # 100

    # Instantiate and use ClassB
    instance_b = factory.ClassB()
    print(instance_b.greet())         # Greetings from ClassB!
    print(instance_b.attribute_b)     # Python Dynamic Class

    # Overwrite 'greet' method in ClassA
    def new_greet_a(self):
        return f"New greetings from {self.__class__.__name__}!"
    factory.overwrite_method('ClassA', 'greet', new_greet_a)

    # Test overwritten method in ClassA
    new_instance_a = factory.ClassA()
    print(new_instance_a.greet())     # New greetings from ClassA!

    # Add and overwrite attributes in ClassB
    factory.add_attribute('ClassB', 'new_attribute_b', 3.1415)
    factory.add_attribute('ClassB', 'attribute_b', 'Updated Python Dynamic Class')
    print(instance_b.new_attribute_b)  # 3.1415
    print(instance_b.attribute_b)      # Updated Python Dynamic Class

    # Manage stored variables
    factory.add_variable('site_name', 'OpenAI')
    factory.add_variable('version', 4.0)
    print(factory.site_name)  # OpenAI
    print(factory.version)     # 4.0

    # Overwrite a stored variable via dot notation
    factory.version = 4.1
    print(factory.version)     # 4.1

    # Add a new stored variable via dot notation
    factory.new_feature = True
    print(factory.new_feature)  # True

    # List stored variables
    print("Stored variables:", factory.list_variables())  # ['site_name', 'version', 'new_feature']

    # Remove a stored variable
    factory.remove_variable('site_name')

    # Attempting to access a removed variable
    try:
        print(factory.site_name)
    except AttributeError as e:
        print(e)  # 'ClassFactory' object has no attribute 'site_name'

    # Remove ClassA from registry
    factory.remove_class('ClassA')
    print("Classes after removal:", factory.list_classes())  # ['ClassB']

    # Attempting to instantiate removed ClassA
    try:
        factory.ClassA()
    except KeyError as e:
        print(e)  # "No class named 'ClassA' found in the registry."

    # Clear all classes from the registry
    factory.clear_registry()
    print("Classes after clearing:", factory.list_classes())  # []

    # Remove remaining variables
    factory.remove_variable('version')
    factory.remove_variable('new_feature')
    print("Stored variables after clearing:", factory.list_variables())  # []
