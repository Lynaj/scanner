import copy
from models.scarped_data import ScarpedData, AddressDict, MetadataDict
from interface import Interface, StepInterface
from controller import SelenimController
from settings import LOGIN_URL, CONTACTINFO_URL, OUTPUT_DATA_PATH
from helper import DOM_IDENTIFIER_TYPE, DOM_ACTION
from google_auth import get_totp_token

class UpWorkScanner:

  def __init__(self,
               upwork_account,
               headless=False):

    # initialize pydantic based data model
    self.upwork_scarped_data = ScarpedData(address = AddressDict(), metadata=MetadataDict())

    # initialize selenium in headless or browser mode depending on init var
    self.browser_controller = SelenimController(headless=headless)

    # initialize instance variables
    self.upwork_account = upwork_account
    self.auth_interface = StepInterface(url=LOGIN_URL, controller=self.browser_controller)
    self.auth_first_optional_interface, self.auth_second_optional_interface = None, None

    # username field
    self.auth_interface.add_step(
      Interface(
        identifier_type=DOM_IDENTIFIER_TYPE.ID,
        identifier_name="login_username",
        action=DOM_ACTION.FILL,
        dom_value=lambda: upwork_account.username,
        controller=self.browser_controller
      )
    )

    # username continue button
    self.auth_interface.add_step(
      Interface(
        identifier_type=DOM_IDENTIFIER_TYPE.ID,
        identifier_name="login_password_continue",
        action=DOM_ACTION.CLICK,
        controller=self.browser_controller
      )
    )

    # password field
    self.auth_interface.add_step(
      Interface(
        identifier_type=DOM_IDENTIFIER_TYPE.ID,
        identifier_name="login_password",
        action=DOM_ACTION.FILL,
        dom_value=lambda: upwork_account.password,
        controller=self.browser_controller
      )
    )

    # password continue button
    self.auth_interface.add_step(
      Interface(
        identifier_type=DOM_IDENTIFIER_TYPE.ID,
        identifier_name="login_control_continue",
        action=DOM_ACTION.CLICK,
        controller=self.browser_controller
      )
    )

    '''
    checks if the second auth password has been delivered
    if so, it might be required
    '''

    if len(upwork_account.secret.strip()) > 0:
      # check if second auth window has been displayed
      self.auth_first_optional_interface = StepInterface(
        optional=True
      )

      # Append the optional interface
      self.auth_interface.add_step(self.auth_first_optional_interface)

      # input secondary auth value
      self.auth_first_optional_interface.add_step(
        Interface(
          identifier_type=DOM_IDENTIFIER_TYPE.ID,
          identifier_name="login_answer",
          action=DOM_ACTION.FILL,
          dom_value=lambda: upwork_account.secret,
          controller=self.browser_controller
        )
      )

      # secondary auth continue button
      self.auth_first_optional_interface.add_step(
        Interface(
          identifier_type=DOM_IDENTIFIER_TYPE.ID,
          identifier_name="login_control_continue",
          action=DOM_ACTION.CLICK,
          controller=self.browser_controller
        )
      )

    '''
    checks if the Google Auth is connected to the account
    '''
    if len(upwork_account.opt_secret.strip()) > 0:
      # check if second auth window has been displayed
      self.auth_second_optional_interface = StepInterface(
        optional=True
      )

      # Append the optional auth interfaces
      self.auth_interface.add_step(self.auth_second_optional_interface)

      # input secondary auth value
      self.auth_second_optional_interface.add_step(
        Interface(
          identifier_type=DOM_IDENTIFIER_TYPE.ID,
          identifier_name="login_otp",
          action=DOM_ACTION.FILL,
          dom_value=lambda: get_totp_token(upwork_account.opt_secret),
          controller=self.browser_controller
        )
      )

      # secondary auth continue button
      self.auth_second_optional_interface.add_step(
        Interface(
          identifier_type=DOM_IDENTIFIER_TYPE.ID,
          identifier_name="login_control_continue",
          action=DOM_ACTION.CLICK,
          controller=self.browser_controller
        )
      )

      # Error message. If is visible, we should repeat all the steps
      self.auth_second_optional_interface.add_step(
        Interface(
          identifier_type=DOM_IDENTIFIER_TYPE.ID,
          identifier_name="otp-message",
          action=DOM_ACTION.READ,
          controller=self.browser_controller,
          repeat=True
        )
      )

    # Prepare profile interface
    self.profile_interface = StepInterface(url=CONTACTINFO_URL, controller=self.browser_controller)

    # Append the optional profile interfaces
    if self.auth_first_optional_interface != None:
      self.profile_interface.add_step(self.auth_first_optional_interface)

    if self.auth_second_optional_interface != None:
      self.auth_second_optional_interfaceDeviceAuth = StepInterface(optional=True)

      # check if second auth window has been displayed
      self.auth_second_optional_interfaceDeviceAuth = StepInterface(
        optional=True
      )

      # Append the optional profile interface
      self.profile_interface.add_step(self.auth_second_optional_interfaceDeviceAuth)

      # input secondary auth value
      self.auth_second_optional_interfaceDeviceAuth.add_step(
        Interface(
          identifier_type=DOM_IDENTIFIER_TYPE.ID,
          identifier_name="deviceAuthOtp_otp",
          action=DOM_ACTION.FILL,
          dom_value=lambda: get_totp_token(upwork_account.opt_secret),
          controller=self.browser_controller
        )
      )

      # secondary auth continue button
      self.auth_second_optional_interfaceDeviceAuth.add_step(
        Interface(
          identifier_type=DOM_IDENTIFIER_TYPE.ID,
          identifier_name="next_continue",
          action=DOM_ACTION.CLICK,
          controller=self.browser_controller
        )
      )

      # Error message. If is visible, we should repeat all the steps
      self.auth_second_optional_interfaceDeviceAuth.add_step(
        Interface(
          identifier_type=DOM_IDENTIFIER_TYPE.ID,
          identifier_name="otp-message",
          action=DOM_ACTION.READ,
          controller=self.browser_controller,
          repeat=True
        )
      )

    '''
      It is the first DOM element in the list
      It might be wise to wait till the page is loaded
    '''
    self.profile_interface.add_step(
      Interface(
        identifier_type=DOM_IDENTIFIER_TYPE.XPATH,
        identifier_name="//div[@data-test='userId']",
        action=DOM_ACTION.READ,
        controller=self.browser_controller,
        getAttribute="innerHTML",
        two_way_data_binding_object=self.upwork_scarped_data,
        two_way_data_binding_attribute='id',
        wait=False
      )
    )

    self.profile_interface.add_step(
      Interface(
        identifier_type=DOM_IDENTIFIER_TYPE.XPATH,
        identifier_name="//div[@data-test='userName']",
        action=DOM_ACTION.READ,
        controller=self.browser_controller,
        getAttribute="innerHTML",
        two_way_data_binding_object=self.upwork_scarped_data,
        two_way_data_binding_attribute='account',
        wait=True
      )
    )

    self.profile_interface.add_step(
      Interface(
        identifier_type=DOM_IDENTIFIER_TYPE.XPATH,
        identifier_name="//span[@data-test='addressStreet']",
        action=DOM_ACTION.READ,
        controller=self.browser_controller,
        getAttribute="innerHTML",
        two_way_data_binding_object=self.upwork_scarped_data,
        two_way_data_binding_attribute='address.line1',
        wait=True
      )
    )

    self.profile_interface.add_step(
      Interface(
        identifier_type=DOM_IDENTIFIER_TYPE.XPATH,
        identifier_name="//span[@data-test='addressStreet']",
        action=DOM_ACTION.READ,
        controller=self.browser_controller,
        getAttribute="innerHTML",
        two_way_data_binding_object=self.upwork_scarped_data,
        two_way_data_binding_attribute='address.line2',
        wait=True
      )
    )

    self.profile_interface.add_step(
      Interface(
        identifier_type=DOM_IDENTIFIER_TYPE.XPATH,
        identifier_name="//span[@data-test='addressCity']",
        action=DOM_ACTION.READ,
        controller=self.browser_controller,
        getAttribute="innerHTML",
        two_way_data_binding_object=self.upwork_scarped_data,
        two_way_data_binding_attribute='address.city',
        wait=True
      )
    )

    self.profile_interface.add_step(
      Interface(
        identifier_type=DOM_IDENTIFIER_TYPE.XPATH,
        identifier_name="//span[@data-test='addressCity']",
        action=DOM_ACTION.READ,
        controller=self.browser_controller,
        getAttribute="innerHTML",
        two_way_data_binding_object=self.upwork_scarped_data,
        two_way_data_binding_attribute='address.state',
        wait=True
      )
    )

    self.profile_interface.add_step(
      Interface(
        identifier_type=DOM_IDENTIFIER_TYPE.XPATH,
        identifier_name="//span[@data-test='addressZip']",
        action=DOM_ACTION.READ,
        controller=self.browser_controller,
        getAttribute="innerHTML",
        two_way_data_binding_object=self.upwork_scarped_data,
        two_way_data_binding_attribute='address.postal_code',
        wait=True
      )
    )

    self.profile_interface.add_step(
      Interface(
        identifier_type=DOM_IDENTIFIER_TYPE.XPATH,
        identifier_name="//span[@data-test='addressCountry']",
        action=DOM_ACTION.READ,
        controller=self.browser_controller,
        getAttribute="innerHTML",
        two_way_data_binding_object=self.upwork_scarped_data,
        two_way_data_binding_attribute='address.country',
        wait=True
      )
    )

    self.profile_interface.add_step(
      Interface(
        identifier_type=DOM_IDENTIFIER_TYPE.XPATH,
        identifier_name="//div[@data-test='phone']",
        action=DOM_ACTION.READ,
        controller=self.browser_controller,
        getAttribute="innerHTML",
        two_way_data_binding_object=self.upwork_scarped_data,
        two_way_data_binding_attribute='phone_number',
        wait=True
      )
    )

  def authenticate(self):
    # Execute the main part
    self.auth_interface.execute()
    self.profile_interface.execute()

    # dump the data
    with open(OUTPUT_DATA_PATH + self.upwork_account.username, 'w') as outfile:
      outfile.writelines(self.upwork_scarped_data.json())