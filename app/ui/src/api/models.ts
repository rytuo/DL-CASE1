export type Coords = [number, number, number, number];

export interface ImageResult {
    items: {
        cls: string,
        xywh: Coords,
        xywhn: Coords,
        xyxy: Coords,
        xyxyn: Coords,
    }[],
}


export default {
    image: async function(image: File) {
        const formData = new FormData();
        formData.append('file', image);
        const res = await fetch("http://0.0.0.0:8000/api/v1/models/:image", {
            method: 'POST',
            body: formData,
        });
        if (res.status === 200) {
            const json = await res.json();
            return json as ImageResult;
        }
        throw new Error(`Error: ${res.statusText}`);
    },
};
