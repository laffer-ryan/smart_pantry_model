scp -i ~/.ssh/yolo-paperspace-key-pair_hyperstack.txt -r ubuntu@38.128.233.103:/home/ubuntu/Users/laffer/Desktop/smart_pantry_model/runs/detect/train ~/Desktop/smart_pantry_model/runs

rsync -avz -e "ssh -i ~/.ssh/yolo-paperspace-key-pair_hyperstack.txt" ubuntu@38.128.233.103:/home/ubuntu/Users/laffer/Desktop/smart_pantry_model/runs/detect/train ~/Desktop/smart_pantry_model/runs/
