import { useState, useMemo, useCallback, useRef, Suspense, use } from 'react'
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



import { useJsApiLoader, StandaloneSearchBox, GoogleMap } from '@react-google-maps/api';

type LatLngLiteral = google.maps.LatLngLiteral;
type DirectionsResult = google.maps.DirectionsResult;
type MapOptions = google.maps.MapOptions;
const GOOGLE_API_KEY = import.meta.env.VITE_API_KEY


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

    const [address, setAddress] = React.useState("")
    const [fetchPromise, setFetchPromise] = useState<Promise<string> | null>(null);


    const handleOpen = () => setOpen(!open);

    const inputref = useRef(null);
    const { isLoaded } = useJsApiLoader({
        id: 'google-map-script',
        googleMapsApiKey: GOOGLE_API_KEY,
        libraries: ["places"]
    })

    const handleOnPlacesChanged = () => {
        let places = inputref.current.getPlaces();
        if (places && places.length > 0) {
            setAddress(places[0].formatted_address);
        }
    }

    const handleSubmit = () => {
        setFetchPromise(getData(address));
    }

    async function getData(address: string) {
        const response = await fetch(`http://127.0.0.1:8080/predict?address=${encodeURIComponent(address)}`);

        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }

        return response.json();
    }

    function FetchAddressResult({ promise }: { promise: Promise<string> }) {
        const result = use(promise); // React suspends here while waiting
        console.log(result)
        return <Typography variant="small" color="white">{result}</Typography>;
    }


    return (

        <div className="flex justify-center bg-[url('./assets/layered-waves-haikei.svg')]" id="background">


            <div className="bg-zinc-950 flex justify-center items-center rounded-2xl mt-30 w-1/2 h-4/5">

                <Button onClick={handleOpen} variant="gradient">
                    Open Modal
                </Button>
                <Dialog open={open} handler={handleOpen} >
                    <DialogBody className="h-100 w-100">
                        {isLoaded && <GoogleMap center={center} options={options} > </GoogleMap>}

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

                        {/* Suspense block only appears after clicking submit */}
                        {fetchPromise && (
                            <Suspense fallback={<Typography variant="small" color="white">Fetching data...</Typography>}>
                                <FetchAddressResult promise={fetchPromise} />
                            </Suspense>
                        )}
                        <Button onClick={handleSubmit} className="mt-6 bg-white text-black" fullWidth>
                            SUBMIT
                        </Button>

                    </form>
                </Card>





            </div>



        </div>

    )
}

export default App



