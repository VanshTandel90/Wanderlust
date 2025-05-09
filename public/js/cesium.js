

Cesium.Ion.defaultAccessToken = mapToken;
const viewer = new Cesium.Viewer('cesiumContainer', {
  terrain: Cesium.Terrain.fromWorldTerrain(),

  sceneMode: Cesium.SceneMode.SCENE2D, // 👈 Forces 2D mode

  animation: false,
  timeline: false,
  infoBox: false,
  sceneModePicker: false,
  navigationHelpButton: false,
  homeButton: false,
  baseLayerPicker: false,
  fullscreenButton: false,
  selectionIndicator: false,
  creditContainer: document.createElement("div")
});

viewer.camera.flyTo({
  destination: Cesium.Cartesian3.fromDegrees(72.8604, 20.4689, 400),
  orientation: {
    heading: Cesium.Math.toRadians(0.0),
    pitch: Cesium.Math.toRadians(-15.0),
  },
});

(async () => {
  const buildingTileset = await Cesium.createOsmBuildingsAsync();
  viewer.scene.primitives.add(buildingTileset);
})();
let searchMarker; // Store reference to remove/update marker

async function geocodeAndFly() {
  const location = document.getElementById("locationInput").value;
  if (!location.trim()) {
    alert("Please enter a location.");
    return;
  }

  const apiKey = openCageToken;

  try {
    const response = await fetch(`https://api.opencagedata.com/geocode/v1/json?q=${encodeURIComponent(location)}&key=${apiKey}`);   //location gives string n apikey converts it to lonngitude n latitude
    const data = await response.json();

    if (data.results.length > 0) {
      const coords = data.results[0].geometry;

      viewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(coords.lng, coords.lat, 10000)
      });

      if (searchMarker) {
        viewer.entities.remove(searchMarker);
      }

      searchMarker = viewer.entities.add({
        position: Cesium.Cartesian3.fromDegrees(coords.lng, coords.lat),
        point: {
          pixelSize: 12,
          color: Cesium.Color.GREEN,
          outlineColor: Cesium.Color.WHITE,
          outlineWidth: 2
        },
        label: {
          text: location,
          font: '14px sans-serif',
          fillColor: Cesium.Color.WHITE,
          style: Cesium.LabelStyle.FILL_AND_OUTLINE,
          outlineWidth: 2,
          showBackground: true,
          backgroundColor: Cesium.Color.BLACK.withAlpha(0.6),
          verticalOrigin: Cesium.VerticalOrigin.TOP,
          pixelOffset: new Cesium.Cartesian2(0, -20)
        }
      });

    } else {
      alert("Location not found!");
    }
  } catch (err) {
    alert("Error fetching location. Please try again later.");
    console.error(err);
  }
}

