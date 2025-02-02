import { useState, useMemo, useCallback, useRef } from 'react'
import React from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import {
  Card,
  Input,
  Button,
  Typography,
  Dialog,
  DialogHeader,
  DialogBody,
  DialogFooter,
} from "@material-tailwind/react";



import { useJsApiLoader, StandaloneSearchBox, GoogleMap  } from '@react-google-maps/api';

type LatLngLiteral = google.maps.LatLngLiteral;
type DirectionsResult = google.maps.DirectionsResult;
type MapOptions = google.maps.MapOptions;


function App() {
  const center = useMemo<LatLngLiteral>(
    () => ({ lat: 43.45, lng: -80.49 }),
    []
  );
  const options = useMemo<MapOptions>(
    () => ({
      mapId: "b181cac70f27f5e6",
      disableDefaultUI: true,
      clickableIcons: false,
    }),
    []
  );

  const [open, setOpen] = React.useState(false);
 
  const handleOpen = () => setOpen(!open);

  const inputref = useRef(null);
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: "AIzaSyB4j6tlYD5ENyzATpxGyceyj0DWhuIZWvI",
    libraries: ["places"]
  })

  const handleOnPlacesChanged = () => {
    let address = inputref.current.getPlaces()
    console.log("address", address)
  }
  


  return (
    
      <div className="flex justify-center bg-[url('./assets/layered-waves-haikei.svg')]" id="background">


         <div className="bg-zinc-950 flex justify-center items-center rounded-2xl mt-30 w-1/2 h-4/5">

         <Button onClick={handleOpen} variant="gradient">
        Open Modal
      </Button>
      <Dialog open={open} handler={handleOpen} >
        <DialogBody className="h-100 w-100"> 
        {isLoaded && <GoogleMap center = {center} options = {options} > </GoogleMap> }

        </DialogBody>
        <DialogFooter>
          <Button
            variant="text"
            color="red"
            onClick={handleOpen}
            className="mr-1"
          >
            <span>Cancel</span>
          </Button>
          <Button variant="gradient" color="green" onClick={handleOpen}>
            <span>Confirm</span>
          </Button>
        </DialogFooter>
      </Dialog>

        <Card color="transparent" shadow={false}>
        <Typography color="white" variant="h2" className="text-center">
          INFERNOWATCH
        </Typography>
        <form className="mt-8 mb-2 w-80 max-w-screen-lg sm:w-96">
          <div className="mb-1 flex flex-col gap-6">
            <Typography variant="h6" color="white" className="-mb-3">
              Address
            </Typography>
            {isLoaded && 
              <StandaloneSearchBox
                  onLoad={(ref) => inputref.current = ref}
                  onPlacesChanged={handleOnPlacesChanged}
                  >
                    <Input
                      size="lg"
                      placeholder="Address"
                      className="!border-white focus:!border-white-300 text-white" // Key classes here
                      labelProps={{
                        className: "before:content-none after:content-none",
                      }}
                    />
              </StandaloneSearchBox>
            }
            
            
         
          </div>

          <Button className="mt-6 bg-white text-black" fullWidth>
            SUBMIT
          </Button>
        
        </form>
      </Card>

      
     
      
      
      </div>  
      
      
      
    </div>

  )
}

export default App



