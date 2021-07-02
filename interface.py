from helper import DOM_ACTION
from exceptions import OptionalException, RepeatException

class Interface(object):

    def __init__(self,
        identifier_type=None,
        identifier_name=None,
        custom_attr_name=None,
        custom_attr_value=None,
        action=None,
        dom_value=None,
        optional=False,
        controller=None,
        repeat=False,
        getAttribute='value',
        two_way_data_binding_object=None,
        two_way_data_binding_attribute=None,
        wait=True
    ):
        self.identifier_type = identifier_type
        self.identifier_name = identifier_name
        self.custom_attr_name = custom_attr_name
        self.custom_attr_value = custom_attr_value
        self.action = action
        self.dom_value = dom_value
        self.optional = optional
        self.controller = controller
        self.getAttribute = getAttribute
        '''
            If repeat = True, it means that we should start the cycle
            from the beginning. This repeat flag is set to True
            only when the DOM element indicates an error ( f.e. wrong MFA code )
        '''
        self.repeat = repeat

        '''
            two_way_data_binding_object contains a reference to the dict defined in the outside of this class
            it is convenient to build this thing up in such a way
            we define only 1 data dict per one session
        '''
        self.two_way_data_binding_object = two_way_data_binding_object

        '''
            two_way_data_binding_attribute represents name of the attribute that we want to manipulate
        '''
        self.two_way_data_binding_attribute = two_way_data_binding_attribute

        # If set to True the time.sleep(x) will be executed
        self.wait = wait

    def __str__(self):
        return str(self.identifier_name)

    def execute(self, optional=None):
        try:
            value = self.controller.execute_action(
                schema=self.identifier_type,
                dom_identifier=self.identifier_name,
                action=self.action,
                value=self.dom_value,
                optional=optional,
                getAttributeValue=self.getAttribute,
                wait=self.wait
            )

            if self.action == DOM_ACTION.READ:
                exec('self.two_way_data_binding_object.' + str(self.two_way_data_binding_attribute) + '=value.strip()')

            if self.repeat == True:
                # Repeat element is visible. We have to repeat a couple of steps
                raise RepeatException()
        except OptionalException:
            raise OptionalException()

        except Exception as e:
            if self.repeat == True:
                # We do expect the repeat DOM element not to be visible
                pass
            else:
                # We propagate the exception
                raise Exception(e)
        else:
            return value

class StepInterface(object):
    steps = None
    url = None
    optional = False
    controller = None

    def __init__(self,
        url=None,
        optional=False,
        controller=None
    ):
        # If URL == None, URL will not be affected
        self.steps = []
        self.url = url
        self.optional = optional
        self.controller = controller

    def add_step(self, step):
        self.steps.append(step)

    def execute(self, optional=None):
        # Change the URL
        if self.url != None:
            self.controller.change_url(self.url)

        index = 0
        number_of_elements = len(self.steps)

        while index < number_of_elements:
            step = self.steps[index]

            try:
                step.execute(optional=self.optional)
            except OptionalException as e:
                '''
                    We want to ignore missing optional elements only when the first
                    DOM element is missing. It means that the particular window is not displayed.
                    Otherwise it is just an error
                '''
                index = number_of_elements

            except RepeatException:
                '''
                    Error DOM element has been revealed. 
                    We have to repeat all the steps assigned to this StepInterface
                '''
                index = 0
            except Exception as e:
                raise Exception(e)
            else:
                index += 1