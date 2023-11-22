%Script that reads a content files and displays annotation info
%/larsson@isy.liu.se 2011

%Set paths to the images and to the annotation file
base = 'F:/trafficSigns/swedishSignsSummer/';
imagePath = fullfile(base,'Set1');
annotationFn = fullfile(imagePath,'annotations.txt');

 %Get content struct from annotation file
content = parseSignAnnotations(annotationFn);      

%For all images with annotation, display content
N = length(content);

for i = 1:N
	fn = fullfile(imagePath,content(i).name);
	try
		img = imread(fn);
		imagesc(img);axis image;
		title(content(i).name);
	catch
		display(['Could not read image: ',fn]);		
	end
	
	try
		%Display content (only bounding boxes)
		displaySigns(content(i).signs,0);
	catch
		display('could not display sign info, something is wrong');
	end	
	pause
end
