from pypylon import pylon

# Initialize the camera
tl_factory = pylon.TlFactory.GetInstance()
camera = pylon.InstantCamera(tl_factory.CreateFirstDevice())
camera.Open()

# Set new resolution (example: 1920x1080)
camera.Width.Value = 1920
camera.Height.Value = 1080

camera.AcquisitionFrameRateEnable.Value = True
camera.AcquisitionFrameRate.Value = 30.0

# Stop and restart grabbing to apply changes
camera.StopGrabbing()
camera.StartGrabbing()

# Now you can start retrieving images with the new resolution
# ...

# Close the camera connection when done
camera.Close()