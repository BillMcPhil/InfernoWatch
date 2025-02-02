import { use, Suspense } from "react";
import { Dialog, DialogBody, IconButton } from "@material-tailwind/react";

async function fetchTile(zoom, x, y, sessionKey, apiKey) {
  return `https://tile.googleapis.com/v1/2dtiles/${zoom}/${x}/${y}?session=${sessionKey}&key=${apiKey}`;
}

function TileImage({ zoom, x, y, sessionKey, apiKey }) {
  const imageUrl = use(fetchTile(zoom, x, y, sessionKey, apiKey));

  return (
    <img
      src={imageUrl}
      alt={`Tile ${x},${y}`}
      className="w-36 h-36 rounded-lg"
    />
  );
}

const Popup = ({ open, onClose, zoom, tiles, sessionKey, apiKey }) => {
  return (
    <Dialog open={open} handler={onClose} size="md">
      {/* Close button */}
      <IconButton
        variant="text"
        className="absolute top-2 right-2"
        onClick={onClose}
      >
        ✖
      </IconButton>

      {/* Dialog Content */}
      <DialogBody className="flex flex-wrap justify-center items-center gap-4 p-6">
        <Suspense fallback={<p>Loading tiles...</p>}>
          {tiles.map(([x, y], index) => (
            <TileImage key={index} zoom={zoom} x={x} y={y} sessionKey={sessionKey} apiKey={apiKey} />
          ))}
        </Suspense>
      </DialogBody>
    </Dialog>
  );
};

export default Popup;

