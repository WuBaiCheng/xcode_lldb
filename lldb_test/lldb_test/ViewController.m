//
//  ViewController.m
//  lldb_test
//
//  Created by 吴伯程 on 2021/7/10.
//

#import "ViewController.h"

@interface ViewController ()

@property (nonatomic, strong) UILabel *label;

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.label = [[UILabel alloc] initWithFrame:CGRectMake(100, 200, 100, 44)];
    self.label.text = @"测试文案";
    self.label.backgroundColor = [UIColor redColor];
    [self.view addSubview:self.label];
}

- (void)viewDidAppear:(BOOL)animated {
    [super viewDidAppear:animated];
    [self method1];
    [ViewController method2];
    [self method3WithP1:@"p1" p2:@"p2"];
    [ViewController method4WithP1:@"p1" p2:@"p2"];
    [self method5WithP1:@"p1" p2:@"p2"];
    [self method6WithP1:@"p1" p2:@"p2"];
}

- (void)method1 {
    NSLog(@"%s", __func__);
}

+ (void)method2 {
    NSLog(@"%s", __func__);
}

- (void)method3WithP1:(id)p1 p2:(id)p2 {
    NSLog(@"%s %@ %@", __func__, p1, p2);
}

+ (void)method4WithP1:(id)p1 p2:(id)p2 {
    NSLog(@"%s %@ %@", __func__, p1, p2);
}

// 格式故意是凌乱的，验证我的正则能否正确处理
-   (  void   )   method5WithP1   :    (  id   )   p1    p2   :   (  id   )   p2     {
    NSLog(@"%s %@ %@", __func__, p1, p2);
}

-   (  void   )   method6WithP1   :    (  id   )   p1    p2   :   (  id   )   p2
     {
    NSLog(@"%s %@ %@", __func__, p1, p2);
}

@end
