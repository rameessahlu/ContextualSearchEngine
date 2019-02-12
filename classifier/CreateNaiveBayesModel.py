


class CreateNaiveBayesModel:
    main_pkg_dir = ''
    train_dir = ''
    test_dir = ''
    metadata_dir = ''
    data_dir = ''
    
    def __init__(self, main_pkg_dir):
        self.main_pkg_dir = main_pkg_dir
        self.train_dir =  os.path.join(os.path.join(main_pkg_dir, 'output'), 'train_data')
        self.test_dir =  os.path.join(os.path.join(main_pkg_dir, 'output'), 'test_data')
        self.test_dir =  os.path.join(os.path.join(main_pkg_dir, 'output'), 'test_data')
        self.data_dir = os.path.join(main_pkg_dir, 'data')