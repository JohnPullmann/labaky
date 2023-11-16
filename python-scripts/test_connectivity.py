from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import os
import ping3

def test_connectivity(logger, Devices):
    """Test connectivity to devices."""
    for device in Devices:
        logger.info(f"Connecting to {device}...")
        try:

            # Ping device
            r = ping3.ping(Devices[device]['host'])

            if r:
                logger.info(f"\tSuccessesfuly pinged {device}")
            else:
                logger.error("\tPing failed")

            # Connect to device
            with ConnectHandler(**Devices[device]) as net_connect:
                logger.info(f"\tConnected to {device}\n")
                
        except (TimeoutError) as error:
            logger.error(f"\tCould not connect to {device}, Connection timed out\n")
        except (NetmikoAuthenticationException) as error:
            logger.error(f"\tCould not connect to {device}, Authentication failed\n")
        except (NetmikoTimeoutException) as error:
            logger.error(error)
            logger.error(f"\tFailed to connect to {device}\n")

    logger.info("Done\n"), 
    return True