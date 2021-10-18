import pytest


def test_warm_ccd_no_devices_error(no_device_response):
    from scripts.warm_ccd import NoDevicesError, main

    with pytest.raises(NoDevicesError):
        main()


def test_warm_ccd_zwo(zwo_device_response):
    from scripts.warm_ccd import main

    zwo_device_response.getNumber.return_value = 20

    # Run the main program
    main()

    zwo_device_response.setNumber.assert_called_once()
    zwo_device_response.sendProperty.assert_called_once()
    zwo_device_response.getNumber.assert_called_once()
    zwo_device_response.setSwitch.assert_not_called()


def test_warm_ccd_qhy(qhy_device_response):
    from scripts.warm_ccd import main

    qhy_device_response.getNumber.return_value = 20

    # Run the main program
    main()

    qhy_device_response.setNumber.assert_called_once()
    qhy_device_response.sendProperty.call_count == 2
    qhy_device_response.getNumber.assert_called_once()
    qhy_device_response.setSwitch.assert_called_once()
